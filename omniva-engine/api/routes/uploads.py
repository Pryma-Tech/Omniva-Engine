"""Upload handling routes for Omniva Engine."""
# TODO: Implement media upload processing and validation.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from workers.manager import WorkerManager
from utils.logger import logger


router = APIRouter()


@router.get("/")
async def list_uploads() -> dict:
    """Return placeholder upload listing."""
    logger.info("TODO: List uploads.")
    return {"message": "TODO: list uploads"}


@router.post("/upload/{project_id}")
async def upload_clip(
    project_id: int,
    data: dict,
    db: Session = Depends(get_db),
) -> dict:
    """
    Trigger an upload manually.
    TODO: Fetch clip from DB.
    TODO: Add validations.
    """
    logger.info("TODO: Trigger upload for project %s.", project_id)
    manager = WorkerManager()
    upload_result = manager.start_upload_task(
        project_id=project_id,
        clip_path=data.get("clip_path", "static/renders/final_clip.mp4"),
        metadata={
            "title": data.get("title", "Placeholder Title"),
            "description": data.get("description", "Placeholder description"),
            "tags": data.get("tags", []),
        },
    )
    return {
        "message": "Upload started (placeholder)",
        "project_id": project_id,
        "input": data,
        "result": upload_result,
    }
