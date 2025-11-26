"""Creator management routes for Omniva Engine (placeholder)."""
# TODO: Connect to real database and scraping subsystem.

from fastapi import APIRouter, Depends, Request

from projects.creators.manager import CreatorManager

router = APIRouter()


def get_creator_manager(request: Request) -> CreatorManager:
    return request.app.state.creator_manager


@router.post("/")
async def add_creator(data: dict, manager: CreatorManager = Depends(get_creator_manager)) -> dict:
    """Create a new creator target."""
    platform = data.get("platform", "tiktok")
    url = data.get("url", "")
    creator = manager.create_creator(platform, url)
    return vars(creator)


@router.post("/{project_id}/assign")
async def assign_creator(project_id: int, data: dict, manager: CreatorManager = Depends(get_creator_manager)) -> dict:
    """Assign creator to a project."""
    creator_id = data.get("creator_id")
    ids = manager.assign_to_project(project_id, creator_id)
    return {"assigned_ids": ids}


@router.get("/{project_id}")
async def list_project_creators(project_id: int, manager: CreatorManager = Depends(get_creator_manager)) -> list:
    """List creators assigned to a project."""
    return [vars(c) for c in manager.list_for_project(project_id)]


@router.get("/")
async def all_creators(manager: CreatorManager = Depends(get_creator_manager)) -> list:
    """Return all creators."""
    return [vars(c) for c in manager.all_creators()]
