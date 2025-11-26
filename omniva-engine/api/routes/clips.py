"""Clip routes for Omniva Engine."""
# TODO: Manage derived clips from downloaded videos.

from typing import List, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from database.repository import ClipRepository
from workers.manager import WorkerManager
from utils.logger import logger


class ClipCreate(BaseModel):
    """Payload for creating a clip."""

    video_id: int
    clip_path: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    score: Optional[int] = None


class ClipUpdate(BaseModel):
    """Payload for updating clip metadata."""

    clip_path: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    score: Optional[int] = None


class ClipResponse(BaseModel):
    """Response schema for clips."""

    id: int
    video_id: int
    clip_path: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    score: Optional[int] = None

    class Config:
        orm_mode = True


router = APIRouter()
CLIP_REPO = ClipRepository()


@router.get("/{video_id}", response_model=List[ClipResponse])
async def list_clips(video_id: int, db: Session = Depends(get_db)) -> List[ClipResponse]:
    """
    List clips for a video.
    TODO: Connect to ClipRepository.list().
    """
    logger.info("TODO: Implement listing clips for video %s.", video_id)
    CLIP_REPO.list(db)
    return []


@router.post("/analyze/{video_id}")
async def analyze_video(video_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Trigger analysis for a video.
    TODO: Fetch video path and keywords from DB.
    TODO: Integrate with actual pipeline.
    """
    logger.info("TODO: Trigger manual analysis for video %s.", video_id)
    manager = WorkerManager()
    # Placeholder, as we do not have real metadata yet.
    analysis = manager.start_analysis_task(
        video_path="placeholder.mp4",
        project_id=0,
        keywords=["placeholder"],
    )
    return {
        "status": "analysis started (placeholder)",
        "video_id": video_id,
        "analysis": analysis,
    }


@router.post("/render/{video_id}")
async def render_clip(video_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Trigger rendering of a video into a clip.
    TODO: Fetch timestamps from analysis results.
    TODO: Save rendered clip to DB.
    """
    logger.info("TODO: Trigger rendering for video %s.", video_id)
    manager = WorkerManager()
    render_result = manager.start_editing_task(
        video_path="placeholder.mp4",
        timestamps={"start": 0, "end": 5},
        output_dir="static/renders",
    )
    return {
        "message": "Rendering started (placeholder)",
        "video_id": video_id,
        "result": render_result,
    }
