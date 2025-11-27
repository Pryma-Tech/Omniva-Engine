"""Pipeline orchestration API."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


@router.post("/run/{project_id}")
async def run_pipeline(project_id: int) -> dict:
    project_manager = registry.get_subsystem("project_manager")
    orchestrator = registry.get_subsystem("orchestrator")

    config = project_manager.get(project_id)
    creators = config.get("creators", [])
    return orchestrator.run_pipeline(project_id, creators)
