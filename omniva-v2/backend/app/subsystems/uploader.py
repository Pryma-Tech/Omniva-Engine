"""Uploader subsystem for Omniva Engine v2 (placeholder)."""

from app.core.registry import registry


class UploaderSubsystem:
    """Placeholder uploader engine."""

    name = "uploader"

    def initialize(self):
        return {"status": "uploader subsystem initialized (placeholder)"}

    def upload(self, renders: list):
        fake_results = []
        for i, render in enumerate(renders):
            fake_results.append(
                {
                    "clip_index": render.get("clip_index", i),
                    "fake_youtube_id": f"FAKE_VIDEO_ID_{i}",
                    "status": "uploaded (placeholder)",
                }
            )
        return {"uploads": fake_results}

    def status(self):
        return {"name": self.name, "status": "ok (placeholder)"}


registry.register_subsystem("uploader", UploaderSubsystem())
