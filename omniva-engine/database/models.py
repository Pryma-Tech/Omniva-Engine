"""Database models for Omniva Engine."""
# TODO: Define ORM models and schemas.

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base

from pydantic import BaseModel


Base = declarative_base()


class Project(Base):
    """SQLAlchemy model describing media projects."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    keywords = Column(Text, nullable=True)
    recency_days = Column(Integer, default=7)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    # TODO: Add relationship to creators and tasks.


class Creator(Base):
    """Social creator definitions tied to projects."""

    __tablename__ = "creators"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    platform = Column(String(32), nullable=False)
    profile_url = Column(String(512), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # TODO: Add relationship back to project and down to videos.


class Video(Base):
    """Original downloaded video assets."""

    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("creators.id"), nullable=False)
    source_url = Column(String(1024), nullable=False)
    download_path = Column(String(1024), nullable=True)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # TODO: Define relationship to clips.


class Clip(Base):
    """Edited clips derived from videos."""

    __tablename__ = "clips"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)
    clip_path = Column(String(1024), nullable=True)
    start_time = Column(Integer, nullable=True)
    end_time = Column(Integer, nullable=True)
    score = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # TODO: Link clip back to its video relationships.


class Task(Base):
    """Background task tracking across the pipeline."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    task_type = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # TODO: Wire up project relationship and scheduling metadata.


class ProjectSchema(BaseModel):
    """Pydantic representation for Project."""

    id: Optional[int]
    name: str
    keywords: Optional[str] = None
    recency_days: Optional[int] = None
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True


class CreatorSchema(BaseModel):
    """Pydantic representation for Creator."""

    id: Optional[int]
    project_id: int
    platform: str
    profile_url: str
    added_at: Optional[datetime]

    class Config:
        orm_mode = True


class VideoSchema(BaseModel):
    """Pydantic representation for Video."""

    id: Optional[int]
    creator_id: int
    source_url: str
    download_path: Optional[str] = None
    metadata_json: Optional[str] = None
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class ClipSchema(BaseModel):
    """Pydantic representation for Clip."""

    id: Optional[int]
    video_id: int
    clip_path: Optional[str] = None
    start_time: Optional[int] = None
    end_time: Optional[int] = None
    score: Optional[int] = None
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class TaskSchema(BaseModel):
    """Pydantic representation for Task."""

    id: Optional[int]
    project_id: int
    task_type: str
    status: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


# TODO: Expand schema definitions with nested relationships once API contracts are clear.
