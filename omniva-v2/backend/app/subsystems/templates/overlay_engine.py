"""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/templates/overlay_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/templates/overlay_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/templates/overlay_engine with cognitive telemetry.

Utilities for generating overlay assets.
"""

import os
import tempfile
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from app.models.template import StyleTemplate


def _load_font(template: StyleTemplate) -> ImageFont.FreeTypeFont:
    try:
        if os.path.isfile(template.font):
            font_path = template.font
        else:
            font_path = template.font
        return ImageFont.truetype(font_path, template.font_size)
    except OSError:
        return ImageFont.load_default()


def generate_text_overlay(text: str, template: StyleTemplate) -> str:
    """Create a PNG with styled caption text."""
    img = Image.new("RGBA", (1080, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = _load_font(template)

    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    x = (1080 - width) // 2
    y = 150 - height // 2

    outline_offsets = [
        (-template.outline_width, 0),
        (template.outline_width, 0),
        (0, -template.outline_width),
        (0, template.outline_width),
    ]
    for dx, dy in outline_offsets:
        draw.text((x + dx, y + dy), text, font=font, fill=template.outline_color)
    draw.text((x, y), text, font=font, fill=template.text_color)

    out_path = tempfile.mktemp(suffix=".png")
    img.save(out_path)
    return out_path


def generate_watermark_overlay(template: StyleTemplate) -> Optional[str]:
    """Return configured watermark path if present."""
    if not template.watermark_path:
        return None
    if not os.path.exists(template.watermark_path):
        return None
    return template.watermark_path
