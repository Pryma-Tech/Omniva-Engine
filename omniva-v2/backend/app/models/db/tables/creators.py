"""Creator ORM model."""

from __future__ import annotations

import uuid

from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.db.base import Base, TimestampMixin
from app.models.db.types import GUID, JSONType


class Creator(TimestampMixin, Base):
    """Managed creator/channel metadata."""

    __tablename__ = "creators"
    __table_args__ = (
        UniqueConstraint("platform", "username", name="uq_creators_platform_username"),
    )

    creator_id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    platform: Mapped[str] = mapped_column(String(32), nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    profile_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata: Mapped[dict | None] = mapped_column(
        MutableDict.as_mutable(JSONType()),
        default=dict,
    )

    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="creator",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Creator {self.platform}:{self.username}>"
