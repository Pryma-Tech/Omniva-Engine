"""Autonomous mode control API."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/autonomous.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/autonomous with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/autonomous with cognitive telemetry.

from __future__ import annotations

import logging
from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.registry import registry

logger = logging.getLogger(__name__)

router = APIRouter()


class AutonomousStateUpdate(BaseModel):
    """Partial update for an autonomous project state."""

    auto_enabled: Optional[bool] = None
    daily_quota: Optional[int] = None


@router.get("/state/{project_id}")
async def get_state(project_id: int) -> dict:
    """Return the current autonomous settings for a project."""
    engine = registry.get_subsystem("autonomous")
    state = engine.store.get_state(project_id)
    logger.info(
        "autonomous.state_get",
        extra={"project_id": project_id, "auto_enabled": state.get("auto_enabled")},
    )
    return state


@router.post("/state/{project_id}")
async def update_state(project_id: int, update: AutonomousStateUpdate) -> dict:
    """Apply a partial state update to a project's autonomous settings."""
    engine = registry.get_subsystem("autonomous")
    state = engine.store.get_state(project_id)
    if update.auto_enabled is not None:
        state["auto_enabled"] = bool(update.auto_enabled)
    if update.daily_quota is not None:
        state["daily_quota"] = int(update.daily_quota)
    result = engine.store.save_state(project_id, state)
    logger.info(
        "autonomous.state_update",
        extra={
            "project_id": project_id,
            "auto_enabled": state.get("auto_enabled"),
            "daily_quota": state.get("daily_quota"),
        },
    )
    return result


@router.post("/start")
async def start_autonomous() -> dict:
    """Start the global autonomous engine."""
    engine = registry.get_subsystem("autonomous")
    engine.start()
    logger.info("autonomous.start")
    return {"status": "autonomous mode started"}


@router.post("/stop")
async def stop_autonomous() -> dict:
    """Stop the global autonomous engine."""
    engine = registry.get_subsystem("autonomous")
    engine.stop()
    logger.info("autonomous.stop")
    return {"status": "autonomous mode stopping"}
