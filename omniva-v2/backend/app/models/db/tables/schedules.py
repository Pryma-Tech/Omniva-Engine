"""Schedule ORM model."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, Text
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.db.base import Base, TimestampMixin
from app.models.db.types import GUID, JSONType


class ScheduleStatus(str, enum.Enum):
    """Scheduling state."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class DecisionSource(str, enum.Enum):
    """Origin of the final schedule."""

    ZENITH = "zenith"
    OPERATOR = "operator_override"
    AUTOMATION = "automation"


class Schedule(TimestampMixin, Base):
    """Committed posting slot for an upload."""

    __tablename__ = "schedules"
    __table_args__ = (
        Index("ix_schedules_clip_id", "clip_id"),
        Index("ix_schedules_final_time", "final_scheduled_time"),
    )

    schedule_id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    clip_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("clips.clip_id", ondelete="RESTRICT"))
    upload_job_id: Mapped[uuid.UUID | None] = mapped_column(GUID(), ForeignKey("upload_jobs.upload_job_id", ondelete="SET NULL"))
    recommended_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    final_scheduled_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    horizon_adjustments: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONType()))
    decision_source: Mapped[DecisionSource | None] = mapped_column(Enum(DecisionSource))
    status: Mapped[ScheduleStatus] = mapped_column(Enum(ScheduleStatus), default=ScheduleStatus.PENDING, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text)

    clip: Mapped["Clip"] = relationship("Clip", back_populates="schedules")
    upload_job: Mapped["UploadJob"] = relationship("UploadJob", back_populates="schedule")

    def __repr__(self) -> str:
        return f"<Schedule {self.schedule_id} status={self.status}>"
