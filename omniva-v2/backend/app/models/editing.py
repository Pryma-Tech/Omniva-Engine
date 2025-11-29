"""Rendered clip models (placeholder)."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/models/editing.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/models/editing with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/models/editing with cognitive telemetry.


from pydantic import BaseModel


class RenderedClip(BaseModel):
    clip_index: int
    start: float
    end: float
    text: str
    fake_ffmpeg_command: str
