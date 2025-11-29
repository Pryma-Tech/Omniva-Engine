"""Pydantic schemas for videos."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class VideoBase(BaseModel):
    post_id: UUID
    file_path: str
    duration_seconds: Optional[float]
    resolution: Optional[str]
    checksum: str


class VideoRead(VideoBase):
    video_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
