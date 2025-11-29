"""Upload job ORM model."""

from __future__ import annotations

import enum
import uuid

from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.db.base import Base, TimestampMixin
from app.models.db.types import GUID, JSONType


class UploadStatus(str, enum.Enum):
    """Upload job lifecycle."""

    PENDING = "pending"
    UPLOADING = "uploading"
    SCHEDULED = "scheduled"
    LIVE = "live"
    ERROR = "error"


class PrivacyStatus(str, enum.Enum):
    """Platform privacy setting."""

    PUBLIC = "public"
    UNLISTED = "unlisted"
    PRIVATE = "private"


class UploadJob(TimestampMixin, Base):
    """Stores metadata for platform publishing."""

    __tablename__ = "upload_jobs"
    __table_args__ = (
        Index("ix_upload_jobs_status", "status"),
        Index("ix_upload_jobs_clip_id", "clip_id"),
    )

    upload_job_id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    clip_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("clips.clip_id", ondelete="RESTRICT"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    keywords: Mapped[list[str] | None] = mapped_column(MutableList.as_mutable(JSONType()))
    scheduled_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    final_scheduled_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    privacy_status: Mapped[PrivacyStatus] = mapped_column(Enum(PrivacyStatus), default=PrivacyStatus.UNLISTED, nullable=False)
    platform: Mapped[str | None] = mapped_column(String(32))
    platform_response_id: Mapped[str | None] = mapped_column(String(64))
    status: Mapped[UploadStatus] = mapped_column(Enum(UploadStatus), default=UploadStatus.PENDING, nullable=False)
    error_detail: Mapped[str | None] = mapped_column(Text)
    metadata: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONType()))

    clip: Mapped["Clip"] = relationship("Clip", back_populates="upload_jobs")
    schedule: Mapped["Schedule"] = relationship("Schedule", back_populates="upload_job", uselist=False)

    def __repr__(self) -> str:
        return f"<UploadJob {self.upload_job_id} status={self.status}>"
