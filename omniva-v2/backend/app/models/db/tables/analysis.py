"""Analysis ORM model."""

from __future__ import annotations

import uuid

from sqlalchemy import Float, ForeignKey, Index, String, Text
from sqlalchemy.ext.mutable import MutableDict, MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.db.base import Base, TimestampMixin
from app.models.db.types import GUID, JSONType


class Analysis(TimestampMixin, Base):
    """Analyzer output per video."""

    __tablename__ = "analysis"
    __table_args__ = (
        Index("ix_analysis_video_id", "video_id"),
        Index("ix_analysis_virality_score", "virality_score"),
    )

    analysis_id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    video_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("videos.video_id", ondelete="CASCADE"))
    transcript: Mapped[str | None] = mapped_column(Text)
    keywords: Mapped[list[str] | None] = mapped_column(MutableList.as_mutable(JSONType()))
    virality_score: Mapped[float | None] = mapped_column(Float)
    relevance_score: Mapped[float | None] = mapped_column(Float)
    language: Mapped[str | None] = mapped_column(String(16))
    raw_ai_output: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONType()))
    model_version: Mapped[str | None] = mapped_column(String(64))

    video: Mapped["Video"] = relationship("Video", back_populates="analyses")

    def __repr__(self) -> str:
        return f\"<Analysis {self.analysis_id} video={self.video_id}>\"
