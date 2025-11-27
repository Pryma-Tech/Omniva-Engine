"""
In-memory job queue with retry tracking.
"""

import logging
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Deque, Dict, Optional

from app.core.registry import get_subsystem

logger = logging.getLogger("omniva_v2")


@dataclass
class Job:
    """Lightweight representation of a queued job."""

    id: int
    type: str
    payload: Dict[str, Any]
    attempts: int = 0
    status: str = "queued"
    result: Optional[Any] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "payload": self.payload,
            "attempts": self.attempts,
            "status": self.status,
            "result": self.result,
            "error": self.error,
        }

    def run(self) -> Any:
        """Execute job logic."""
        return _execute_job(self)


class JobQueue:
    """Simple FIFO queue with retry support."""

    def __init__(self) -> None:
        self._queue: Deque[Job] = deque()
        self._jobs: Dict[int, Job] = {}
        self._next_id = 1

    def enqueue(self, job_type: str, payload: Dict[str, Any]) -> Job:
        job = Job(id=self._next_id, type=job_type, payload=payload)
        self._queue.append(job)
        self._jobs[job.id] = job
        self._next_id += 1
        logger.info("Enqueued job %s (#%s)", job.type, job.id)
        return job

    def dequeue(self) -> Optional[Job]:
        if not self._queue:
            return None
        job = self._queue.popleft()
        job.status = "processing"
        return job

    def finish_job(self, job_id: int, result: Any) -> None:
        job = self._jobs.get(job_id)
        if not job:
            return
        job.status = "completed"
        job.result = result
        logger.info("Job %s completed", job_id)

    def fail_job(self, job_id: int, error: str) -> None:
        job = self._jobs.get(job_id)
        if not job:
            return
        job.attempts += 1
        job.error = error
        if job.attempts < 3:
            job.status = "retry"
            self._queue.append(job)
            logger.warning("Job %s failed (%s). Retrying (%s/3).", job_id, error, job.attempts)
        else:
            job.status = "failed"
            logger.error("Job %s failed permanently: %s", job_id, error)

    def __len__(self) -> int:
        return len(self._queue)


def _execute_job(job: Job) -> Any:
    """Route job execution to the correct subsystem."""
    if job.type == "analyze":
        analysis = get_subsystem("analysis")
        return analysis.analyze_transcript(
            filepath=job.payload.get("filepath"),
            project_id=job.payload.get("project_id", 0),
            keywords=job.payload.get("keywords", []),
        )
    if job.type == "edit_clip":
        editor = get_subsystem("editing")
        return editor.edit_clip(
            analysis_filepath=job.payload.get("analysis_filepath", ""),
            project_id=job.payload.get("project_id", 0),
            top_n=job.payload.get("top_n", 1),
        )
    if job.type == "upload_clip":
        uploader = get_subsystem("uploader")
        return uploader.upload_clips(
            clips=job.payload.get("clips", []),
            project_id=job.payload.get("project_id", 0),
        )
    if job.type == "transcribe":
        transcription = get_subsystem("transcription")
        return transcription.transcribe_file(
            filepath=job.payload.get("filepath"),
            project_id=job.payload.get("project_id", 0),
        )
    if job.type == "download_url":
        downloader = get_subsystem("download")
        return downloader.download_url(
            url=job.payload.get("url"),
            project_id=job.payload.get("project_id", 0),
        )
    if job.type == "start_pipeline":
        project_id = job.payload.get("project_id", 0)
        links = job.payload.get("links", [])
        for link in links:
            job_queue.enqueue("download_url", {"url": link, "project_id": project_id})
        return {"status": "pipeline triggered", "project_id": project_id}
    if job.type == "run_pipeline":
        return {
            "status": "pipeline executed (placeholder)",
            "project_id": job.payload.get("project_id"),
        }
    return {"status": "unknown job", "type": job.type}


job_queue = JobQueue()


def get_job_queue() -> JobQueue:
    return job_queue
