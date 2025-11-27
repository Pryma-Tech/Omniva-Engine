"""Intelligence engine API routes."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


def _engine():
    return registry.get_subsystem("intelligence")


@router.get("/status")
async def get_status() -> dict:
    return _engine().status()


@router.post("/mode/{mode}")
async def set_mode(mode: str) -> dict:
    return _engine().set_mode(mode)


@router.get("/posting-time/{project_id}")
async def get_posting_time(project_id: int) -> dict:
    return _engine().choose_posting_time(project_id)


@router.get("/posting-stats/{project_id}")
async def get_posting_stats(project_id: int) -> dict:
    return _engine().get_posting_stats(project_id)


@router.post("/apply-schedule/{project_id}")
async def apply_schedule(project_id: int) -> dict:
    intel = _engine()
    scheduler = registry.get_subsystem("scheduler")
    recommendation = intel.choose_posting_time(project_id)
    hour = recommendation.get("recommended_hour", 18)
    cron = f"0 {hour} * * *"
    config = scheduler.configure_project(project_id, enabled=True, cron=cron)
    return {
        "project_id": project_id,
        "recommended": recommendation,
        "applied_cron": cron,
        "scheduler_config": config,
    }


@router.get("/trending/{project_id}")
async def get_trending(project_id: int) -> dict:
    intel = _engine()
    return intel.get_trending_keywords(project_id)
