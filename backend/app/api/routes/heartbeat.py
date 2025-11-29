"""Heartbeat control API."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/heartbeat", tags=["heartbeat"])


@router.post("/start")
async def heartbeat_start() -> dict:
    # TODO(omniva-v0.1): Validate caller permissions before starting heartbeat loop.
    # TODO(omniva-v0.2): Emit Stardust entry capturing start reason and context.
    return registry.heartbeat.start()


@router.post("/stop")
async def heartbeat_stop() -> dict:
    # TODO(omniva-v0.1): Ensure graceful shutdown of scheduled tasks.
    # TODO(omniva-v0.2): Add optional timeout parameter for controlled drain.
    return registry.heartbeat.stop()


@router.get("/status")
async def heartbeat_status() -> dict:
    # TODO(omniva-v0.1): Include next scheduled run and last execution timestamp.
    # TODO(omniva-v0.2): Surface health metrics pulled from heartbeat subsystem.
    return {"running": registry.heartbeat.running}
