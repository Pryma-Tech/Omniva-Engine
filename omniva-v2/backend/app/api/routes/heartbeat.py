"""Heartbeat control API."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/heartbeat.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/heartbeat with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/heartbeat with cognitive telemetry.


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
