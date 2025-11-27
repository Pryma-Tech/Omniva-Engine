"""Editing subsystem for Omniva Engine v2 (placeholder)."""

from typing import Any, Dict, List

from app.core.registry import registry


class EditingSubsystem:
    """Placeholder editing engine."""

    name = "editing"

    def initialize(self) -> Dict[str, str]:
        return {"status": "editing subsystem initialized (placeholder)"}

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
