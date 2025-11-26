"""Analysis subsystem for Omniva Engine v2 (placeholder)."""

from typing import List

from app.core.registry import registry
from app.core.event_bus import event_bus
from app.core.job_queue import job_queue
from app.models.pipeline import ClipCandidate


class AnalysisSubsystem:
    """Placeholder analysis engine."""

    name = "analysis"

    def initialize(self):
        event_bus.subscribe("transcription_complete", self.on_transcription_ready)
        return {"status": "analysis subsystem initialized (placeholder)"}

    def on_transcription_ready(self, payload: dict):
        job_queue.enqueue("analyze_transcript", payload)

    def analyze_transcript(self, project_id: int, transcript: dict) -> List[ClipCandidate]:
        return [
            ClipCandidate(start=0.0, end=3.0, text="Placeholder highlight #1", score=0.82),
            ClipCandidate(start=3.0, end=8.0, text="Placeholder highlight #2", score=0.67),
        ]

    def status(self):
        return {"name": self.name, "status": "ok (placeholder)"}

