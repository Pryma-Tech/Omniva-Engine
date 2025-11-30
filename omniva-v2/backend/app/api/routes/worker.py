"""Worker subsystem API."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/worker.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/worker with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/worker with cognitive telemetry.


from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


@router.get("/status")
async def worker_status() -> dict:
    worker = registry.get_subsystem("worker")
    return worker.status()


@router.get("/heartbeat")
async def worker_heartbeat() -> dict:
    worker = registry.get_subsystem("worker")
    return worker.heartbeat().dict()


@router.post("/step")
async def worker_step() -> dict:
    worker = registry.get_subsystem("worker")
    return worker.step()


@router.post("/run_batch")
async def worker_batch(data: dict | None = None) -> dict:
    worker = registry.get_subsystem("worker")
    limit = (data or {}).get("limit", 5)
    return worker.run_batch(limit)
