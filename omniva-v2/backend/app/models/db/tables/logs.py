"""Structured log ORM model."""

from __future__ import annotations

import enum
import uuid

from sqlalchemy import Enum, Index, String, Text
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import Mapped, mapped_column

from app.models.db.base import Base, TimestampMixin
from app.models.db.types import GUID, JSONType


class LogLevel(str, enum.Enum):
    """Log severity levels."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"


class LogEntry(TimestampMixin, Base):
    """Operational/cognitive log row."""

    __tablename__ = "logs"
    __table_args__ = (
        Index("ix_logs_source", "source"),
        Index("ix_logs_level", "level"),
        Index("ix_logs_created_at_desc", "created_at"),
    )

    log_id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(String(64), nullable=False)
    level: Mapped[LogLevel] = mapped_column(Enum(LogLevel), default=LogLevel.INFO, nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    metadata: Mapped[dict | None] = mapped_column(MutableDict.as_mutable(JSONType()))
    trace_id: Mapped[uuid.UUID | None] = mapped_column(GUID())
    stardust_id: Mapped[uuid.UUID | None] = mapped_column(GUID())

    def __repr__(self) -> str:
        return f"<LogEntry {self.log_id} {self.level} {self.source}>"
