"""Pydantic schemas for upload jobs."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.db.tables.upload_jobs import PrivacyStatus, UploadStatus


class UploadJobBase(BaseModel):
    clip_id: UUID
    title: str = Field(..., max_length=255)
    description: Optional[str]
    keywords: Optional[List[str]]
    scheduled_time: Optional[datetime]
    final_scheduled_time: Optional[datetime]
    privacy_status: PrivacyStatus = PrivacyStatus.UNLISTED
    platform: Optional[str]
    platform_response_id: Optional[str]
    status: UploadStatus = UploadStatus.PENDING
    error_detail: Optional[str]
    metadata: Optional[Dict[str, Any]]


class UploadJobRead(UploadJobBase):
    upload_job_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
