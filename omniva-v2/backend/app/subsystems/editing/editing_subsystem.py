"""
FFmpeg-powered editing subsystem.
"""

import json
import os
from typing import Any, Dict, List

from app.core.event_bus import event_bus
from app.core.job_queue import job_queue
from app.core.registry import registry
from app.models.analysis import ClipCandidate

from .ffmpeg_util import convert_to_vertical, cut_clip
from .subtitles import burn_subtitles
from .templates import ClipTemplate


class EditingSubsystem:
    """Render clips from analyzed transcript segments."""

    name = "editing"

    def __init__(self) -> None:
        self.template = ClipTemplate("default")

    def initialize(self) -> Dict[str, str]:
        return {"status": "editing subsystem initialized"}

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

        for index, candidate in enumerate(selected_candidates):
            base_name = f"clip_{index}"
            cut_path = os.path.join(output_dir, f"{base_name}_cut.mp4")
            vertical_path = os.path.join(output_dir, f"{base_name}_vertical.mp4")
            final_path = os.path.join(output_dir, f"{base_name}_final.mp4")

            cut_clip(source_video, cut_path, candidate.start, candidate.end)
            convert_to_vertical(cut_path, vertical_path)
            templated_path = self.template.apply(vertical_path, vertical_path)
            burn_subtitles(templated_path, final_path, candidate.text)
            rendered_paths.append(final_path)

        result = {
            "project_id": project_id,
            "analysis_filepath": analysis_filepath,
            "clips": rendered_paths,
        }
        event_bus.publish("editing_complete", result)
        job_queue.enqueue("upload_clips", {"project_id": project_id, "clips": rendered_paths})
        return result

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}


registry.register_subsystem("editing", EditingSubsystem())
