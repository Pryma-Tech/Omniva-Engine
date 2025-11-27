"""Discovery API routes."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


@router.get("/project/{project_id}")
async def discover_project(project_id: int) -> dict:
    discovery = registry.get_subsystem("discovery")
    new_posts = discovery.discover_for_project(project_id)
    return {"project_id": project_id, "new_posts": new_posts}
