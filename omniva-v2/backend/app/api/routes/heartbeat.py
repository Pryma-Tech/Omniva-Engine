"""Heartbeat control API."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/heartbeat.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/heartbeat with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/heartbeat with cognitive telemetry.

import logging

from fastapi import APIRouter, HTTPException

from app.core.registry import registry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/heartbeat", tags=["heartbeat"])


def _get_heartbeat():
    heartbeat = getattr(registry, "heartbeat", None)
    if heartbeat is None:
        logger.error("heartbeat.unavailable")
        raise HTTPException(status_code=503, detail="heartbeat subsystem unavailable")
    return heartbeat


@router.post("/start")
async def heartbeat_start() -> dict:
    """Start the global heartbeat loop."""
    heartbeat = _get_heartbeat()
    result = heartbeat.start()
    logger.info("heartbeat.api_start", extra={"result": result})
    return result


@router.post("/stop")
async def heartbeat_stop() -> dict:
    """Stop the global heartbeat loop."""
    heartbeat = _get_heartbeat()
    result = heartbeat.stop()
    logger.info("heartbeat.api_stop", extra={"result": result})
    return result


@router.get("/status")
async def heartbeat_status() -> dict:
    """Report whether the heartbeat loop is running."""
    heartbeat = _get_heartbeat()
    status = {"running": heartbeat.running}
    logger.info("heartbeat.api_status", extra=status)
    return status
