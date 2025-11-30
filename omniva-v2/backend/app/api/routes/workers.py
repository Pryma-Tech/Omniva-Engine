"""Worker engine control API."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/workers.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/workers with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/workers with cognitive telemetry.


import asyncio

from fastapi import APIRouter

from app.core.worker_engine import WorkerEngine

router = APIRouter()
workers = WorkerEngine(concurrency=3)


@router.post("/start")
async def start_workers() -> dict:
    asyncio.create_task(workers.start())
    return {"status": "workers started"}


@router.post("/stop")
async def stop_workers() -> dict:
    workers.stop()
    return {"status": "workers stopping"}
