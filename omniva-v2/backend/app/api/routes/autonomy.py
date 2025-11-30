"""Autonomy kernel control routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/autonomy.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/autonomy with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/autonomy with cognitive telemetry.


from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/autonomy", tags=["autonomy"])


@router.post("/start/{project_id}")
async def autonomy_start(project_id: int) -> dict:
    return registry.autonomy.start_project(project_id)


@router.post("/stop/{project_id}")
async def autonomy_stop(project_id: int) -> dict:
    return registry.autonomy.stop_project(project_id)


@router.post("/pause/{project_id}")
async def autonomy_pause(project_id: int) -> dict:
    return registry.autonomy.pause_project(project_id)


@router.post("/resume/{project_id}")
async def autonomy_resume(project_id: int) -> dict:
    return registry.autonomy.resume_project(project_id)
