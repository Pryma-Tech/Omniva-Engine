"""Worker subsystem API (placeholder)."""

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
