"""Video routes for Omniva Engine."""
# TODO: Manage scraping and persistence of source videos.

from typing import List, Optional

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from database.repository import VideoRepository
from workers.scraper.scraper_controller import ScraperController
from utils.logger import logger


class VideoCreate(BaseModel):
    """Payload for manually creating a video record."""

    source_url: str
    download_path: Optional[str] = None
    metadata_json: Optional[str] = None


class VideoUpdate(BaseModel):
    """Payload for updating stored video metadata."""

    download_path: Optional[str] = None
    metadata_json: Optional[str] = None


class VideoResponse(BaseModel):
    """Response schema for videos."""

    id: int
    creator_id: int
    source_url: str
    download_path: Optional[str] = None
    metadata_json: Optional[str] = None

    class Config:
        orm_mode = True


router = APIRouter()
VIDEO_REPO = VideoRepository()


@router.get("/{creator_id}", response_model=List[VideoResponse])
async def list_videos(creator_id: int, db: Session = Depends(get_db)) -> List[VideoResponse]:
    """
    List all videos for a creator.
    TODO: Connect to VideoRepository.list() with filters.
    """
    logger.info("TODO: Implement listing videos for creator %s.", creator_id)
    VIDEO_REPO.list(db)
    return []


@router.post(
    "/scan/{creator_id}",
    status_code=status.HTTP_202_ACCEPTED,
)
async def scan_videos(
    creator_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """
    Trigger video scan placeholder endpoint.
    TODO: Kick off scraper worker and persist new videos.
    """
    logger.info("TODO: Implement scanning videos for creator %s.", creator_id)
    controller = ScraperController()
    # TODO: Load real creator/project info from database.
    placeholder_creator = {
        "id": creator_id,
        "platform": "tiktok",
        "profile_url": "https://example.com/profile",
    }
    scrape_results = controller.scrape_creator(
        platform=placeholder_creator["platform"],
        project_id=0,
        creator=placeholder_creator,
        recency_days=7,
    )
    VIDEO_REPO.create(db, data={"creator_id": creator_id})
    return {"message": "Scraping started (placeholder)", "results": scrape_results}
