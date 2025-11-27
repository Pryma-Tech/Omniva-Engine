"""Scheduler API endpoints."""

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
