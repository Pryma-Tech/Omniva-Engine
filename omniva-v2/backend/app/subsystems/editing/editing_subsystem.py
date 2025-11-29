"""
FFmpeg-powered editing subsystem.
"""

import asyncio
import json
import os
import shutil
from typing import Any, Dict, List

from app.core.event_bus import event_bus
from app.core.job_queue import job_queue
from app.core.registry import registry
from app.models.analysis import ClipCandidate
from app.models.template import StyleTemplate
from app.subsystems.templates.overlay_engine import (
    generate_text_overlay,
    generate_watermark_overlay,
)
from app.subsystems.templates.template_engine import TemplateEngine
from app.subsystems.templates.template_store import TemplateStore

from .ffmpeg_util import convert_to_vertical, cut_clip
from .subtitles import burn_subtitles


class EditingSubsystem:
    """Render clips from analyzed transcript segments."""

    name = "editing"

    def __init__(self) -> None:
        self.template_store = TemplateStore()
        if self.template_store.load_template("default") is None:
            self.template_store.save_template(StyleTemplate(name="default"))
        self.template_engine = TemplateEngine()

    def initialize(self) -> Dict[str, str]:
        return {"status": "editing subsystem initialized"}

    async def render(self, project_id: int, source_file: str, transcript: str) -> str:
        """
        Lightweight render wrapper for the autonomous loop.
        """
        output_dir = os.path.join("storage", "projects", str(project_id), "clips")
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(source_file))[0]
        output_path = os.path.join(output_dir, f"{base_name}_rendered.mp4")
        await asyncio.to_thread(shutil.copy, source_file, output_path)
        # attach transcript for future overlays (not used yet)
        meta_path = os.path.join(output_dir, f"{base_name}_transcript.txt")
        def _write_transcript() -> None:
            with open(meta_path, "w", encoding="utf-8") as handle:
                handle.write(transcript or "")

        await asyncio.to_thread(_write_transcript)
        return output_path

    def edit_clip(self, analysis_filepath: str, project_id: int, top_n: int = 1) -> Dict[str, Any]:
        """Render the top N clip candidates into share-ready videos."""
        if not analysis_filepath or not os.path.exists(analysis_filepath):
            return {"error": "analysis file not found", "analysis_filepath": analysis_filepath}

        with open(analysis_filepath, "r", encoding="utf-8") as analysis_file:
            raw_candidates: List[Dict[str, Any]] = json.load(analysis_file)

        if not raw_candidates:
            return {"error": "no candidates found", "analysis_filepath": analysis_filepath}

        selected_candidates = [ClipCandidate(**candidate) for candidate in raw_candidates[:top_n]]

        raw_video_dir = os.path.join("storage", "projects", str(project_id), "raw")
        if not os.path.exists(raw_video_dir):
            return {"error": "raw directory missing", "path": raw_video_dir}
        raw_files = [
            os.path.join(raw_video_dir, file_name)
            for file_name in os.listdir(raw_video_dir)
            if os.path.isfile(os.path.join(raw_video_dir, file_name))
        ]
        if not raw_files:
            return {"error": "no raw videos found", "path": raw_video_dir}

        output_dir = os.path.join("storage", "projects", str(project_id), "clips")
        os.makedirs(output_dir, exist_ok=True)

        rendered_paths: List[str] = []
        source_video = raw_files[0]

        template = self.template_store.load_template("default") or StyleTemplate(name="default")

        for index, candidate in enumerate(selected_candidates):
            base_name = f"clip_{index}"
            cut_path = os.path.join(output_dir, f"{base_name}_cut.mp4")
            vertical_path = os.path.join(output_dir, f"{base_name}_vertical.mp4")
            final_path = os.path.join(output_dir, f"{base_name}_final.mp4")

            cut_clip(source_video, cut_path, candidate.start, candidate.end)
            convert_to_vertical(cut_path, vertical_path)
            burn_subtitles(vertical_path, final_path, candidate.text)

            text_overlay = generate_text_overlay(candidate.text, template)
            watermark_overlay = generate_watermark_overlay(template)
            styled_path = final_path.replace("_final", "_styled")
            self.template_engine.apply_template(final_path, styled_path, text_overlay, watermark_overlay)
            if text_overlay and os.path.exists(text_overlay):
                os.remove(text_overlay)

            rendered_paths.append(styled_path)

        result = {
            "project_id": project_id,
            "analysis_filepath": analysis_filepath,
            "clips": rendered_paths,
        }
        event_bus.publish("editing_complete", result)
        job_queue.enqueue(
            "upload_clip",
            {
                "project_id": project_id,
                "clips": rendered_paths,
            },
        )
        return result

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}


registry.register_subsystem("editing", EditingSubsystem())
