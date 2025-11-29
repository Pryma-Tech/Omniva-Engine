"""Stardust metadata ORM model."""

from __future__ import annotations

import uuid

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.db.base import Base, TimestampMixin
from app.models.db.types import GUID, JSONType


class StardustMetadata(TimestampMixin, Base):
    """Immutable provenance packets linking events, evidence, and decisions."""

    __tablename__ = "stardust_metadata"
    __table_args__ = (
        Index("ix_stardust_entity_lookup", "entity_type", "entity_id"),
    )

    stardust_id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=False)
    lineage: Mapped[dict] = mapped_column(JSONType(), nullable=False)
    decision_chain: Mapped[dict | None] = mapped_column(JSONType())
    trace_id: Mapped[uuid.UUID | None] = mapped_column(GUID())

    def __repr__(self) -> str:
        return f"<StardustMetadata {self.stardust_id} entity={self.entity_type}:{self.entity_id}>"
