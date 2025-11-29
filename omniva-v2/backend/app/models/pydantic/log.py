"""Pydantic schemas for structured logs."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.db.tables.logs import LogLevel


class LogEntryRead(BaseModel):
    log_id: UUID
    source: str
    level: LogLevel
    message: str
    metadata: Optional[Dict[str, Any]]
    trace_id: Optional[UUID]
    stardust_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
