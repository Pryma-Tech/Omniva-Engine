"""In-memory job queue (placeholder)."""
# TODO: Replace with distributed queue (Redis, RabbitMQ, etc.).

from collections import deque
from dataclasses import dataclass
from typing import Any, Deque, Dict

from .registry import get_subsystem

import logging

logger = logging.getLogger("omniva_v2")


@dataclass
class Job:
    id: int
    type: str
    payload: Dict[str, Any]
    result: Any | None = None

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "type": self.type, "payload": self.payload, "result": self.result}


class JobQueue:
    """Simple FIFO queue."""

    def __init__(self):
        self._queue: Deque[Job] = deque()
        self._next_id = 1

    def enqueue(self, job_type: str, payload: Dict[str, Any]) -> None:
        logger.info("Enqueue job %s (placeholder)", job_type)
        self._queue.append(Job(id=self._next_id, type=job_type, payload=payload))
        self._next_id += 1

    def dequeue(self) -> Job | None:
        if not self._queue:
            return None
        return self._queue.popleft()

    def process(self, job: Job) -> Any:
        logger.info("Processing job %s (placeholder)", job.type)
        if job.type == "analyze_transcript":
            analysis = get_subsystem("analysis")
            result = analysis.analyze_transcript(
                project_id=job.payload.get("project_id"),
                transcript=job.payload.get("transcript"),
            )
            job.result = [c.dict() for c in result]
        elif job.type == "render_clips":
            editing = get_subsystem("editing")
            candidates = job.payload.get("candidates", [])
            job.result = editing.render_candidates(candidates)
        elif job.type == "upload_clips":
            uploader = get_subsystem("uploader")
            renders = job.payload.get("renders", [])
            job.result = uploader.upload(renders)
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


JOB_QUEUE = JobQueue()

def get_job_queue() -> JobQueue:
    return JOB_QUEUE

job_queue = JOB_QUEUE
