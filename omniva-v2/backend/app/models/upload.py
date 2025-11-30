"""Upload result models."""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/models/upload with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/models/upload with cognitive telemetry.


from pydantic import BaseModel


class UploadResult(BaseModel):
    clip_index: int
    fake_youtube_id: str
    status: str
