"""Discovery API routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/discovery.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/discovery with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/discovery with cognitive telemetry.


from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


@router.get("/project/{project_id}")
async def discover_project(project_id: int) -> dict:
    discovery = registry.get_subsystem("discovery")
    new_posts = discovery.discover_for_project(project_id)
    return {"project_id": project_id, "new_posts": new_posts}
