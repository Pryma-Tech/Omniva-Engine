"""Worker engine control API."""

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
