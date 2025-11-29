"""Edit job ORM model."""

from __future__ import annotations

import enum
import uuid

from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Index, Text
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.db.base import Base, TimestampMixin
from app.models.db.types import GUID, JSONType


class EditJobStatus(str, enum.Enum):
    """Edit job lifecycle."""

    PENDING = "pending"
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"
    CANCELLED = "cancelled"


class EditJob(TimestampMixin, Base):
    """Represents FFmpeg editing pipelines per clip."""

    __tablename__ = "edit_jobs"
    __table_args__ = (
        Index("ix_edit_jobs_status", "status"),
        Index("ix_edit_jobs_clip_id", "clip_id"),
    )

    edit_job_id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    clip_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("clips.clip_id", ondelete="RESTRICT"))
    operations: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSONType()), nullable=False)
    ffmpeg_commands: Mapped[list[str] | None] = mapped_column(MutableList.as_mutable(JSONType()))
    gpu_required: Mapped[bool] = mapped_column(default=False)
    estimated_duration_seconds: Mapped[float | None] = mapped_column(Float)
    status: Mapped[EditJobStatus] = mapped_column(Enum(EditJobStatus), default=EditJobStatus.PENDING, nullable=False)
    error_detail: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    clip: Mapped["Clip"] = relationship("Clip", back_populates="edit_jobs")

    def __repr__(self) -> str:
        return f"<EditJob {self.edit_job_id} status={self.status}>"
