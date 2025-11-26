"""Database package for Omniva Engine."""
# TODO: Initialize connections and metadata.

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base


DATABASE_URL = "sqlite:///./omniva.db"

# TODO: Externalize connection string via configuration module.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Initialize database metadata if needed."""
    # TODO: Integrate Alembic migrations instead of create_all.
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Provide a scoped session for FastAPI dependencies."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: Add helpers for migrations, indexing, and advanced options.
