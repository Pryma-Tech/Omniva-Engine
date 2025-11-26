"""Autonomous mode routes (placeholder)."""
# TODO: Secure these endpoints and integrate real background jobs.

from fastapi import APIRouter, Depends, Request

from autonomous.manager import AutonomousModeManager

router = APIRouter()


def get_autonomous_manager(request: Request) -> AutonomousModeManager:
    return request.app.state.autonomous_manager


@router.post("/enable/{project_id}")
async def enable_auto(project_id: int, manager: AutonomousModeManager = Depends(get_autonomous_manager)) -> dict:
    return manager.enable(project_id)


@router.post("/disable/{project_id}")
async def disable_auto(project_id: int, manager: AutonomousModeManager = Depends(get_autonomous_manager)) -> dict:
    return manager.disable(project_id)


@router.get("/status/{project_id}")
async def status_auto(project_id: int, manager: AutonomousModeManager = Depends(get_autonomous_manager)) -> dict:
    return {"project_id": project_id, "enabled": manager.is_enabled(project_id)}


@router.post("/tick")
async def auto_tick(manager: AutonomousModeManager = Depends(get_autonomous_manager)) -> dict:
    return manager.tick()
