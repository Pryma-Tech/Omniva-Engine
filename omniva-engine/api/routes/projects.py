"""Project management routes for Omniva Engine."""
# TODO: Define CRUD endpoints for video projects.

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def list_projects() -> dict:
    """List all projects (placeholder)."""
    return {"message": "TODO: list projects"}
