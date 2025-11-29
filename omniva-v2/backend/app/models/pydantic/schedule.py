"""Pydantic schemas for schedules."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.db.tables.schedules import DecisionSource, ScheduleStatus


class ScheduleBase(BaseModel):
    clip_id: UUID
    upload_job_id: Optional[UUID]
    recommended_time: Optional[datetime]
    final_scheduled_time: Optional[datetime]
    horizon_adjustments: Optional[Dict[str, Any]]
    decision_source: Optional[DecisionSource]
    status: ScheduleStatus = ScheduleStatus.PENDING
    notes: Optional[str]


class ScheduleRead(ScheduleBase):
    schedule_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
