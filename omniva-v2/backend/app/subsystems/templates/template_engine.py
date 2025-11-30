# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/templates/template_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/templates/template_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/templates/template_engine with cognitive telemetry.

"\"\"\"Applies visual templates via FFmpeg overlays.\"\"\""

import os
from typing import Optional

import ffmpeg


class TemplateEngine:
    """Combine overlays and source footage."""

    def apply_template(
        self,
        input_path: str,
        output_path: str,
        text_overlay_path: Optional[str],
        watermark_path: Optional[str],
    ) -> str:
        """Apply overlays and export to output."""
        stream = ffmpeg.input(input_path)
        video = stream.video
        audio = stream.audio

        if text_overlay_path and os.path.exists(text_overlay_path):
            video = video.overlay(
                ffmpeg.input(text_overlay_path),
                x="(main_w-overlay_w)/2",
                y="main_h - overlay_h - 50",
            )

        if watermark_path and os.path.exists(watermark_path):
            video = video.overlay(
                ffmpeg.input(watermark_path),
                x=30,
                y=30,
                enable="between(t,0,20000)",
            )

        (
            ffmpeg.output(video, audio, output_path)
            .overwrite_output()
            .run(quiet=True)
        )
        return output_path
