"""Transcription subsystem for Omniva Engine v2 (placeholder)."""

from app.core.registry import registry


class TranscriptionSubsystem:
    """Placeholder transcription engine."""

    name = "transcription"

    def initialize(self) -> dict:
        return {"status": "transcription subsystem initialized (placeholder)"}

    def status(self) -> dict:
        return {"name": self.name, "status": "ok (placeholder)"}


registry.register_subsystem("transcription", TranscriptionSubsystem())
