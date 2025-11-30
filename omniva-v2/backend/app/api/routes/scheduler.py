"""Scheduler API endpoints."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/scheduler.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/scheduler with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/scheduler with cognitive telemetry.


from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


@router.get("/project/{project_id}")
async def get_project_schedule(project_id: int) -> dict:
    scheduler = registry.get_subsystem("scheduler")
    return scheduler.get_project_schedule(project_id)


@router.post("/project/{project_id}")
async def set_project_schedule(project_id: int, data: dict) -> dict:
    scheduler = registry.get_subsystem("scheduler")
    return scheduler.configure_project(
        project_id,
        data.get("enabled", False),
        data.get("cron", "0 */6 * * *"),
    )
