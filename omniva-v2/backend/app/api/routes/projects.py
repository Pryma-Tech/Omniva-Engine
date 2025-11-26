"""Project routes (placeholder)."""

from fastapi import APIRouter
from typing import List

from ...models.project import Project

router = APIRouter()

FAKE_PROJECTS: List[Project] = [
    Project(project_id=1, name="Demo Project", keywords=["ai", "clips"], recency_days=7, active=True)
]


@router.get("/", response_model=List[Project])
async def list_projects() -> List[Project]:
    """Return placeholder projects."""
    return FAKE_PROJECTS


@router.post("/", response_model=Project)
async def create_project(project: Project) -> Project:
    FAKE_PROJECTS.append(project)
    return project
