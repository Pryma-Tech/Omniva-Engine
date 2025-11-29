"""Shared pytest fixtures for data-layer tests."""

from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models.db.base import Base
from app.models.db.tables import *  # noqa: F401,F403


@pytest.fixture()
def session() -> Session:
    """Provide an isolated in-memory DB session."""
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
