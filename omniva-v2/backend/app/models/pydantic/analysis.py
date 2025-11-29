"""Pydantic schemas for analysis records."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel


class AnalysisBase(BaseModel):
    video_id: UUID
    transcript: Optional[str]
    keywords: Optional[List[str]]
    virality_score: Optional[float]
    relevance_score: Optional[float]
    language: Optional[str]
    raw_ai_output: Optional[Dict[str, Any]]
    model_version: Optional[str]


class AnalysisRead(AnalysisBase):
    analysis_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
