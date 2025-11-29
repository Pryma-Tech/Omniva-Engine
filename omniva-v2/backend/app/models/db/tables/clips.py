"""Clip ORM model."""

from __future__ import annotations

import enum
import uuid

from sqlalchemy import Enum, Float, ForeignKey, Index, Integer, String
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.db.base import Base, TimestampMixin
from app.models.db.types import GUID, JSONType


class ClipStatus(str, enum.Enum):
    """Lifecycle for clip candidates."""

    PENDING = "pending"
    PROMOTED = "promoted"
    REJECTED = "rejected"
    ARCHIVED = "archived"


class Clip(TimestampMixin, Base):
    """Candidate segments derived from analysis."""

    __tablename__ = "clips"
    __table_args__ = (
        Index("ix_clips_video_id", "video_id"),
        Index("ix_clips_confidence_desc", "confidence"),
    )

    clip_id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    video_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("videos.video_id", ondelete="CASCADE"))
    start_time: Mapped[float] = mapped_column(Float, nullable=False)
    end_time: Mapped[float] = mapped_column(Float, nullable=False)
    confidence: Mapped[float | None] = mapped_column(Float)
    subject_focus: Mapped[str | None] = mapped_column(String(128))
    faces_detected: Mapped[int | None] = mapped_column(Integer)
    semantic_tags: Mapped[list[str] | None] = mapped_column(MutableList.as_mutable(JSONType()))
    pantheon_votes: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONType()))
    lattice_priority: Mapped[float | None] = mapped_column(Float)
    metadata: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONType()))
    status: Mapped[ClipStatus] = mapped_column(Enum(ClipStatus), default=ClipStatus.PENDING, nullable=False)

    video: Mapped["Video"] = relationship("Video", back_populates="clips")
    edit_jobs: Mapped[list["EditJob"]] = relationship("EditJob", back_populates="clip")
    upload_jobs: Mapped[list["UploadJob"]] = relationship("UploadJob", back_populates="clip")
    schedules: Mapped[list["Schedule"]] = relationship("Schedule", back_populates="clip")

    def __repr__(self) -> str:
        return f"<Clip {self.clip_id} status={self.status}>"
