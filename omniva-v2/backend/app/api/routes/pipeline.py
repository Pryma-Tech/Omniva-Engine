"""Pipeline orchestration API."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/pipeline.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/pipeline with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/pipeline with cognitive telemetry.


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
