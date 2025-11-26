"""Upload handling routes for Omniva Engine."""
# TODO: Implement media upload processing and validation.

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def list_uploads() -> dict:
    """Return placeholder upload listing."""
    return {"message": "TODO: list uploads"}
