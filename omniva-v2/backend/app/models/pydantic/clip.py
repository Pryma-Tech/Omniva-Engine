"""Pydantic schemas for clips."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.db.tables.clips import ClipStatus


class ClipBase(BaseModel):
    video_id: UUID
    start_time: float = Field(..., ge=0)
    end_time: float = Field(..., gt=0)
    confidence: Optional[float]
    subject_focus: Optional[str]
    faces_detected: Optional[int]
    semantic_tags: Optional[List[str]]
    pantheon_votes: Optional[Dict[str, float]]
    lattice_priority: Optional[float]
    metadata: Optional[Dict[str, Any]]
    status: ClipStatus = ClipStatus.PENDING


class ClipRead(ClipBase):
    clip_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
