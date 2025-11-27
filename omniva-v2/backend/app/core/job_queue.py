"""In-memory job queue (placeholder)."""
# TODO: Replace with distributed queue (Redis, RabbitMQ, etc.).

import logging
from collections import deque
from dataclasses import dataclass
from typing import Any, Deque, Dict, Optional

from app.core.registry import get_subsystem

logger = logging.getLogger("omniva_v2")


@dataclass
class Job:
    """Lightweight representation of a queued job."""

    id: int
    type: str
    payload: Dict[str, Any]
    result: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "type": self.type, "payload": self.payload, "result": self.result}


class JobQueue:
    """Simple FIFO queue."""

    def __init__(self) -> None:
        self._queue: Deque[Job] = deque()
        self._next_id = 1

    def enqueue(self, job_type: str, payload: Dict[str, Any]) -> None:
        logger.info("Enqueue job %s (placeholder)", job_type)
        self._queue.append(Job(id=self._next_id, type=job_type, payload=payload))
        self._next_id += 1

    def dequeue(self) -> Optional[Job]:
        if not self._queue:
            return None
        return self._queue.popleft()

    def process(self, job: Job) -> Any:
        """Process a job and attach the placeholder result."""
        logger.info("Processing job %s (placeholder)", job.type)
        if job.type == "analyze":
            analysis = get_subsystem("analysis")
            job.result = analysis.analyze_transcript(
                filepath=job.payload.get("filepath"),
                project_id=job.payload.get("project_id", 0),
                keywords=job.payload.get("keywords", []),
            )
        elif job.type == "edit_clip":
            editor = get_subsystem("editing")
            job.result = editor.edit_clip(
                analysis_filepath=job.payload.get("analysis_filepath", ""),
                project_id=job.payload.get("project_id", 0),
                top_n=job.payload.get("top_n", 1),
            )
        elif job.type == "upload_clip":
            uploader = get_subsystem("uploader")
            job.result = uploader.upload_clips(
                clips=job.payload.get("clips", []),
                project_id=job.payload.get("project_id", 0),
            )
        elif job.type == "transcribe":
            transcription = get_subsystem("transcription")
            job.result = transcription.transcribe_file(
                filepath=job.payload.get("filepath"),
                project_id=job.payload.get("project_id", 0),
            )
        elif job.type == "download_url":
            downloader = get_subsystem("download")
            job.result = downloader.download_url(
                url=job.payload.get("url"),
                project_id=job.payload.get("project_id", 0),
            )
        elif job.type == "run_pipeline":
            job.result = {
                "status": "pipeline executed (placeholder)",
                "project_id": job.payload.get("project_id"),
            }
        else:
            job.result = {"status": "unknown job", "type": job.type}
        return job.result

    def __len__(self) -> int:
        return len(self._queue)


job_queue = JobQueue()


def get_job_queue() -> JobQueue:
    return job_queue
