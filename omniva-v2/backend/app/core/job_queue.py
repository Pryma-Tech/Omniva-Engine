"""In-memory job queue (placeholder)."""
# TODO: Replace with distributed queue (Redis, RabbitMQ, etc.).

from collections import deque
from typing import Any, Deque, Dict
from .registry import get_subsystem

import logging

logger = logging.getLogger("omniva_v2")


class JobQueue:
    """Simple FIFO queue."""

    def __init__(self):
        self._queue: Deque[Dict[str, Any]] = deque()

    def enqueue(self, job_type: str, payload: Dict[str, Any]) -> None:
        logger.info("Enqueue job %s (placeholder)", job_type)
        self._queue.append({"type": job_type, "payload": payload})

    def dequeue(self) -> Dict[str, Any] | None:
        if not self._queue:
            return None
        job = self._queue.popleft()
        logger.info("Dequeue job %s (placeholder)", job["type"])
        if job["type"] == "analyze_transcript":
            analysis = get_subsystem("analysis")
            result = analysis.analyze_transcript(
                project_id=job["payload"].get("project_id"),
                transcript=job["payload"].get("transcript"),
            )
            job["result"] = [c.dict() for c in result]
        elif job["type"] == "render_clips":
            editing = get_subsystem("editing")
            candidates = job["payload"].get("candidates", [])
            job["result"] = editing.render_candidates(candidates)
        elif job["type"] == "upload_clips":
            uploader = get_subsystem("uploader")
            renders = job["payload"].get("renders", [])
            job["result"] = uploader.upload(renders)
        return job

    def __len__(self) -> int:
        return len(self._queue)


JOB_QUEUE = JobQueue()

def get_job_queue() -> JobQueue:
    return JOB_QUEUE
job_queue = JOB_QUEUE
