"""Style template models."""

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
