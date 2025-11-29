"""Post ORM model."""

from __future__ import annotations

import uuid

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.db.base import Base, TimestampMixin
from app.models.db.types import GUID, JSONType


class Post(TimestampMixin, Base):
    """Individual social post fetched from a creator feed."""

    __tablename__ = "posts"
    __table_args__ = (
        UniqueConstraint("platform", "platform_post_id", name="uq_posts_platform_source"),
        Index("ix_posts_creator_posted_at", "creator_id", "posted_at"),
    )

    post_id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    creator_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("creators.creator_id", ondelete="CASCADE"))
    platform: Mapped[str] = mapped_column(String(32), nullable=False)
    platform_post_id: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    downloaded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    raw_metadata: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONType()))

    creator: Mapped["Creator"] = relationship("Creator", back_populates="posts")
    videos: Mapped[list["Video"]] = relationship(
        "Video",
        back_populates="post",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Post {self.platform}:{self.platform_post_id}>"
