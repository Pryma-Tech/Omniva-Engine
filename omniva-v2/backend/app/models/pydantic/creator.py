"""Pydantic schemas for creators."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CreatorBase(BaseModel):
    platform: str = Field(..., max_length=32)
    username: str = Field(..., max_length=255)
    profile_url: Optional[str]
    metadata: Optional[Dict[str, Any]]


class CreatorCreate(CreatorBase):
    """Payload for creating/updating creators."""


class CreatorRead(CreatorBase):
    creator_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
