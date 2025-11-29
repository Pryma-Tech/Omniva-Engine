"""Pydantic schemas for Stardust metadata."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class StardustPacket(BaseModel):
    stardust_id: UUID
    entity_type: str
    entity_id: UUID
    lineage: Dict[str, Any]
    decision_chain: Optional[Dict[str, Any]]
    trace_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
