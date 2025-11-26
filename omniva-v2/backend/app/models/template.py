"""Style template models (placeholder)."""

from pydantic import BaseModel


class StyleTemplate(BaseModel):
    name: str
    aspect_ratio: str = "9:16"
    color_palette: str = "default"
    subtitle_style: str = "default"
    transition_style: str = "cut"
    audio_style: str = "none"
