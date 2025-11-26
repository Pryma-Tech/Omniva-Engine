"""Project routes (placeholder)."""

from typing import List

from fastapi import APIRouter

from app.models.project import Project

router = APIRouter()

_FAKE_PROJECTS: List[Project] = [
    Project(project_id=1, name="Demo Project", keywords=["ai", "clips"], recency_days=7, active=True)
]


@router.get("/")
async def list_projects() -> list:
    return [project.dict() for project in _FAKE_PROJECTS]


@router.post("/")
async def create_project(project: Project) -> dict:
    _FAKE_PROJECTS.append(project)
    return project.dict()
