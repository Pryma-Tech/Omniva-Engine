"""Heartbeat control API."""

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import require_control_token
from app.core.registry import registry

router = APIRouter(prefix="/heartbeat", tags=["heartbeat"])


def _heartbeat():
    heartbeat = getattr(registry, "heartbeat", None)
    if heartbeat is None:
        raise HTTPException(status_code=503, detail="heartbeat subsystem unavailable")
    return heartbeat


@router.post("/start")
async def heartbeat_start(_: str = Depends(require_control_token)) -> dict:
    """Start the global heartbeat loop."""
    heartbeat = _heartbeat()
    return heartbeat.start()


@router.post("/stop")
async def heartbeat_stop(_: str = Depends(require_control_token)) -> dict:
    """Stop the heartbeat loop after draining pending tasks."""
    heartbeat = _heartbeat()
    return await heartbeat.stop()


@router.get("/status")
async def heartbeat_status() -> dict:
    """Report scheduler state, including next scheduled actions."""
    heartbeat = _heartbeat()
    return {"running": heartbeat.running, "schedule": heartbeat.schedule_snapshot()}
