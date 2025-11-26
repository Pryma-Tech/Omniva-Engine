"""Worker heartbeat models (placeholder)."""

from pydantic import BaseModel


class WorkerHeartbeat(BaseModel):
    worker_id: str
    timestamp: float
    status: str
