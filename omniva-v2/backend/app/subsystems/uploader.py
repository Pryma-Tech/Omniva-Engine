"""Uploader subsystem for Omniva Engine v2 (placeholder)."""

from app.core.registry import registry
from app.core.event_bus import event_bus
from app.core.job_queue import job_queue


class UploaderSubsystem:
    """Placeholder uploader engine."""

    name = "uploader"

    def initialize(self):
        event_bus.subscribe("clips_rendered", self.on_renders_ready)
        return {"status": "uploader subsystem initialized (placeholder)"}

    def on_renders_ready(self, payload: dict):
        job_queue.enqueue("upload_clips", payload)

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
