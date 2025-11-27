"""Autonomous mode control API."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


@router.get("/state/{project_id}")
async def get_state(project_id: int) -> dict:
    engine = registry.get_subsystem("autonomous")
    return engine.store.get_state(project_id)


@router.post("/state/{project_id}")
async def update_state(project_id: int, data: dict) -> dict:
    engine = registry.get_subsystem("autonomous")
    state = engine.store.get_state(project_id)
    if "auto_enabled" in data:
        state["auto_enabled"] = bool(data["auto_enabled"])
    if "daily_quota" in data:
        state["daily_quota"] = int(data["daily_quota"])
    return engine.store.save_state(project_id, state)


@router.post("/start")
async def start_autonomous() -> dict:
    engine = registry.get_subsystem("autonomous")
    engine.start()
    return {"status": "autonomous mode started"}


@router.post("/stop")
async def stop_autonomous() -> dict:
    engine = registry.get_subsystem("autonomous")
    engine.stop()
    return {"status": "autonomous mode stopping"}
