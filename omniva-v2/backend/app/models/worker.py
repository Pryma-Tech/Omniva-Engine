"""Worker heartbeat models."""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/models/worker with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/models/worker with cognitive telemetry.


from pydantic import BaseModel


class WorkerHeartbeat(BaseModel):
    worker_id: str
    timestamp: float
    status: str
