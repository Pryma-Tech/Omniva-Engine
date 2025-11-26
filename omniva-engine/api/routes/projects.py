"""Project management routes for Omniva Engine (placeholder)."""
# TODO: Replace with database-backed CRUD operations.

from fastapi import APIRouter, Depends, Request

from projects.manager import ProjectManager


router = APIRouter()


def get_project_manager(request: Request) -> ProjectManager:
    """Return shared ProjectManager from app state."""
    manager: ProjectManager = request.app.state.project_manager
    return manager


@router.get("/")
async def list_projects(pm: ProjectManager = Depends(get_project_manager)) -> list:
    """List in-memory projects (placeholder)."""
    return [vars(p) for p in pm.list()]


@router.post("/")
async def create_project(data: dict, pm: ProjectManager = Depends(get_project_manager)) -> dict:
    """Create project (placeholder)."""
    name = data.get("name", "Untitled Project")
    keywords = data.get("keywords", [])
    recency = data.get("recency_days", 7)
    project = pm.create(name, keywords, recency)
    return vars(project)


@router.get("/{project_id}")
async def get_project(project_id: int, pm: ProjectManager = Depends(get_project_manager)) -> dict | None:
    """Return project by id."""
    project = pm.get(project_id)
    return vars(project) if project else None


@router.post("/{project_id}/keywords")
async def update_keywords(project_id: int, data: dict, pm: ProjectManager = Depends(get_project_manager)) -> dict | None:
    """Update project keywords."""
    project = pm.update_keywords(project_id, data.get("keywords", []))
    return vars(project) if project else None


@router.post("/{project_id}/creators")
async def add_creator(project_id: int, data: dict, pm: ProjectManager = Depends(get_project_manager)) -> dict | None:
    """Add creator to project."""
    project = pm.add_creator(project_id, data)
    return vars(project) if project else None


@router.post("/{project_id}/toggle")
async def toggle_active(project_id: int, pm: ProjectManager = Depends(get_project_manager)) -> dict | None:
    """Toggle active flag."""
    project = pm.toggle_active(project_id)
    return vars(project) if project else None
