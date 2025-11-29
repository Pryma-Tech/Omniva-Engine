"""Style template models."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/models/template.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/models/template with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/models/template with cognitive telemetry.


from typing import Optional

from pydantic import BaseModel


class StyleTemplate(BaseModel):
    """Represents typography and overlay settings for clips."""

    name: str
    font: str = "Arial"
    font_size: int = 48
    text_color: str = "white"
    outline_color: str = "black"
    outline_width: int = 2
    watermark_path: Optional[str] = None
