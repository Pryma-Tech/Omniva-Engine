"""Pydantic schemas for edit jobs."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.db.tables.edit_jobs import EditJobStatus


class EditJobBase(BaseModel):
    clip_id: UUID
    operations: Dict[str, Any]
    ffmpeg_commands: Optional[List[str]]
    gpu_required: bool = False
    estimated_duration_seconds: Optional[float]
    status: EditJobStatus = EditJobStatus.PENDING
    error_detail: Optional[str]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]


class EditJobRead(EditJobBase):
    edit_job_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
