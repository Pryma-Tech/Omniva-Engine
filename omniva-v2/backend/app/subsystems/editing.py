"""Editing subsystem for Omniva Engine v2 (placeholder)."""

from typing import Any, Dict, List

from app.core.registry import registry
from app.core.event_bus import event_bus
from app.core.job_queue import job_queue


class EditingSubsystem:
    """Placeholder editing engine."""

    name = "editing"

    def initialize(self) -> Dict[str, str]:
        event_bus.subscribe("analysis_complete", self.on_analysis_ready)
        return {"status": "editing subsystem initialized (placeholder)"}

    def on_analysis_ready(self, payload: dict) -> None:
        job_queue.enqueue("render_clips", payload)

    def render_candidates(self, candidates: list) -> Dict[str, Any]:
        fake_outputs: List[Dict[str, Any]] = []
        for i, candidate in enumerate(candidates):
            fake_outputs.append(
                {
                    "clip_index": i,
                    "start": candidate.get("start", 0.0),
                    "end": candidate.get("end", 0.0),
                    "text": candidate.get("text", "placeholder"),
                    "fake_ffmpeg_command": (
                        f"ffmpeg -i INPUT.mp4 -ss {candidate.get('start', 0.0)} -to {candidate.get('end', 0.0)} "
                        "-vf 'scale=1080:1920' "
                        f"rendered_clip_{i}.mp4"
                    ),
                }
            )
        return {"renders": fake_outputs}

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok (placeholder)"}


registry.register_subsystem("editing", EditingSubsystem())
