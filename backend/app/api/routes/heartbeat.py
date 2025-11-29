"""Heartbeat control API."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/heartbeat", tags=["heartbeat"])


@router.post("/start")
async def heartbeat_start() -> dict:
    return registry.heartbeat.start()


@router.post("/stop")
async def heartbeat_stop() -> dict:
    return registry.heartbeat.stop()


@router.get("/status")
async def heartbeat_status() -> dict:
    return {"running": registry.heartbeat.running}
