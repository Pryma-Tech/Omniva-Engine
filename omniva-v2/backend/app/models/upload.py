"""Upload result models (placeholder)."""

from pydantic import BaseModel


class UploadResult(BaseModel):
    clip_index: int
    fake_youtube_id: str
    status: str
