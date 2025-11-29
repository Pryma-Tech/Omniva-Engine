"""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/core/job_queue.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/core/job_queue with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/core/job_queue with cognitive telemetry.

Persistent job queue with retry tracking and execution helpers.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import uuid4

from app.core.registry import get_subsystem


class JobWrapper:
    """Lightweight proxy that exposes run()/metadata helpers."""

    def __init__(self, data: Dict[str, Any]) -> None:
        self._data = data

    @property
    def id(self) -> str:
        return self._data["id"]

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    @property
    def type(self) -> str:
        return self._data["type"]

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)

    def run(self) -> Any:
        return _execute_job(self._data)


class JobQueue:
    """File-backed job queue with retry state."""

    def __init__(self) -> None:
        self.queue: List[str] = []
        self.jobs: Dict[str, Dict[str, Any]] = {}
        self.storage_dir = os.path.join("storage", "jobs")
        os.makedirs(self.storage_dir, exist_ok=True)
        self._load_existing()

    def _path(self, job_id: str) -> str:
        return os.path.join(self.storage_dir, f"{job_id}.json")

    def _load_existing(self) -> None:
        for file_name in os.listdir(self.storage_dir):
            if not file_name.endswith(".json"):
                continue
            job_id = file_name.replace(".json", "")
            with open(self._path(job_id), "r", encoding="utf-8") as job_file:
                job = json.load(job_file)
                self.jobs[job_id] = job
                if job.get("status") in {"queued", "retrying", "running"}:
                    self.queue.append(job_id)

    def enqueue(self, job_type: str, payload: Dict[str, Any]) -> str:
        job_id = str(uuid4())
        job = {
            "id": job_id,
            "type": job_type,
            "payload": payload,
            "created": datetime.utcnow().isoformat(),
            "status": "queued",
            "attempts": 0,
        }
        self.jobs[job_id] = job
        self.queue.append(job_id)
        self._save(job)
        return job_id

    def dequeue(self) -> Optional[JobWrapper]:
        if not self.queue:
            return None
        job_id = self.queue.pop(0)
        job = self.jobs[job_id]
        job["status"] = "running"
        job["started"] = datetime.utcnow().isoformat()
        self._save(job)
        return JobWrapper(job)

    def finish_job(self, job_id: str, result: Any) -> None:
        job = self.jobs.get(job_id)
        if not job:
            return
        job["status"] = "done"
        job["finished"] = datetime.utcnow().isoformat()
        job["result"] = result
        self._save(job)

    def fail_job(self, job_id: str, error: str) -> None:
        job = self.jobs.get(job_id)
        if not job:
            return
        job["attempts"] += 1
        job["status"] = "failed"
        job["error"] = error
        job["finished"] = datetime.utcnow().isoformat()
        self._save(job)

    def retry_job(self, job_id: str, backoff_seconds: int) -> None:
        job = self.jobs.get(job_id)
        if not job:
            return
        job["attempts"] += 1
        job["status"] = "retrying"
        job["retry_after"] = (datetime.utcnow() + timedelta(seconds=backoff_seconds)).isoformat()
        self._save(job)

    def requeue(self, job_id: str) -> None:
        job = self.jobs.get(job_id)
        if not job:
            return
        job["status"] = "queued"
        job.pop("retry_after", None)
        self.queue.append(job_id)
        self._save(job)

    def _save(self, job: Dict[str, Any]) -> None:
        with open(self._path(job["id"]), "w", encoding="utf-8") as job_file:
            json.dump(job, job_file, indent=2)


def _execute_job(job: Dict[str, Any]) -> Any:
    job_type = job["type"]
    payload = job.get("payload", {})
    if job_type == "analyze":
        analysis = get_subsystem("analysis")
        return analysis.analyze_transcript(
            filepath=payload.get("filepath"),
            project_id=payload.get("project_id", 0),
            keywords=payload.get("keywords", []),
        )
    if job_type == "edit_clip":
        editor = get_subsystem("editing")
        return editor.edit_clip(
            analysis_filepath=payload.get("analysis_filepath", ""),
            project_id=payload.get("project_id", 0),
            top_n=payload.get("top_n", 1),
        )
    if job_type == "upload_clip":
        uploader = get_subsystem("uploader")
        return uploader.upload_clips(
            clips=payload.get("clips", []),
            project_id=payload.get("project_id", 0),
        )
    if job_type == "transcribe":
        transcription = get_subsystem("transcription")
        return transcription.transcribe_file(
            filepath=payload.get("filepath"),
            project_id=payload.get("project_id", 0),
        )
    if job_type == "download_url":
        downloader = get_subsystem("download")
        return downloader.download_url(
            url=payload.get("url"),
            project_id=payload.get("project_id", 0),
        )
    if job_type == "start_pipeline":
        orchestrator = get_subsystem("orchestrator")
        project_manager = get_subsystem("project_manager")
        config = project_manager.get(payload.get("project_id", 0))
        creators = config.get("creators", [])
        return orchestrator.run_pipeline(payload.get("project_id", 0), creators)
    if job_type == "run_pipeline":
        return {"status": "pipeline executed (placeholder)", "project_id": payload.get("project_id")}
    return {"status": "unknown job", "type": job_type}


job_queue = JobQueue()


def get_job_queue() -> JobQueue:
    return job_queue
