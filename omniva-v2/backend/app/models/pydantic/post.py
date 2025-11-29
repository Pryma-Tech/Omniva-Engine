"""Pydantic schemas for posts."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class PostBase(BaseModel):
    platform: str = Field(..., max_length=32)
    platform_post_id: str = Field(..., max_length=255)
    url: str
    posted_at: Optional[datetime]
    downloaded_at: Optional[datetime]
    raw_metadata: Optional[Dict[str, Any]]


class PostCreate(PostBase):
    creator_id: UUID


class PostRead(PostBase):
    post_id: UUID
    creator_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
