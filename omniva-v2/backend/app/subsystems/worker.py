"""Worker subsystem for manual job control."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/worker.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/worker with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/worker with cognitive telemetry.


import time
from typing import Any, Dict

from app.core.event_bus import event_bus
from app.core.job_queue import job_queue
from app.core.registry import registry
from app.models.worker import WorkerHeartbeat


class WorkerSubsystem:
    """Expose heartbeat + manual stepping endpoints."""

    name = "worker"

    def __init__(self) -> None:
        self.last_heartbeat = time.time()

    def initialize(self) -> Dict[str, str]:
        return {"status": "worker subsystem initialized (placeholder)"}

    def heartbeat(self) -> WorkerHeartbeat:
        self.last_heartbeat = time.time()
        return WorkerHeartbeat(worker_id="primary", timestamp=self.last_heartbeat, status="ok (manual)")

    def step(self) -> Dict[str, Any]:
        job = job_queue.dequeue()
        if job is None:
            return {"status": "no jobs", "processed": False}
        try:
            result = job.run()
            job_queue.finish_job(job.id, result)
            event_bus.publish("worker_job_complete", {"job_id": job.id, "type": job.type})
            return {"status": "processed job", "processed": True, "job": job.to_dict(), "result": result}
        except Exception as exc:  # pylint: disable=broad-except
            job_queue.fail_job(job.id, str(exc))
            return {"status": "job failed", "processed": False, "error": str(exc), "job": job.to_dict()}

    def run_batch(self, limit: int = 5) -> Dict[str, Any]:
        processed = []
        for _ in range(limit):
            out = self.step()
            processed.append(out)
            if not out.get("processed", False):
                break
        return {"batch": processed}

    def status(self) -> Dict[str, Any]:
        return {"name": self.name, "last_heartbeat": self.last_heartbeat, "status": "ok"}


registry.register_subsystem("worker", WorkerSubsystem())
