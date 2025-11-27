"""Project configuration API."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


def _pm():
    return registry.get_subsystem("project_manager")


@router.get("/")
async def list_projects() -> list:
    manager = _pm()
    return manager.list_all()


@router.get("/{project_id}")
async def get_project(project_id: int) -> dict:
    manager = _pm()
    return manager.get(project_id)


@router.post("/{project_id}")
async def update_project(project_id: int, data: dict) -> dict:
    manager = _pm()
    project = manager.get(project_id)
    if "creators" in data:
        project["creators"] = data["creators"]
    if "keywords" in data:
        project["keywords"] = data["keywords"]
    return manager.save(project_id, project)
