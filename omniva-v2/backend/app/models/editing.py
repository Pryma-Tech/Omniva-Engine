"""Rendered clip models (placeholder)."""

from pydantic import BaseModel


class RenderedClip(BaseModel):
    clip_index: int
    start: float
    end: float
    text: str
    fake_ffmpeg_command: str
