"""Database engine/session helpers."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import load_config
from app.models.db.base import Base

config = load_config()

# NOTE: SQLite is the default developer target; switch DATABASE_URL for Postgres in production.
engine = create_engine(
    config.database_url,
    echo=config.database_echo,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)


def init_db() -> None:
    """Create tables when running against SQLite or during local bootstrap."""
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a managed session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Context manager for scripts/tests."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:  # pragma: no cover - helper wrapper
        session.rollback()
        raise
    finally:
        session.close()
