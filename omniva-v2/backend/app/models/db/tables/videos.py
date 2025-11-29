"""Video ORM model."""

from __future__ import annotations

import uuid

from sqlalchemy import Float, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.db.base import Base, TimestampMixin
from app.models.db.types import GUID


class Video(TimestampMixin, Base):
    """Normalized media asset derived from a post."""

    __tablename__ = "videos"
    __table_args__ = (
        UniqueConstraint("checksum", name="uq_videos_checksum"),
        Index("ix_videos_post_id", "post_id"),
    )

    video_id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    post_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("posts.post_id", ondelete="CASCADE"))
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    duration_seconds: Mapped[float | None] = mapped_column(Float)
    resolution: Mapped[str | None] = mapped_column(String(32))
    checksum: Mapped[str] = mapped_column(String(128), nullable=False)

    post: Mapped["Post"] = relationship("Post", back_populates="videos")
    analyses: Mapped[list["Analysis"]] = relationship(
        "Analysis",
        back_populates="video",
        cascade="all, delete-orphan",
    )
    clips: Mapped[list["Clip"]] = relationship(
        "Clip",
        back_populates="video",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Video {self.video_id} checksum={self.checksum[:8]}>"
