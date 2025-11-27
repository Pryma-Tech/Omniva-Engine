"""
Real transcription subsystem powered by Whisper.
"""

import json
import os
from typing import Any, Dict

from app.core.event_bus import event_bus
from app.core.registry import registry

from .normalizer import normalize_segments
from .whisper_engine import WhisperTranscriber


class TranscriptionSubsystem:
    """Run local Whisper inference and persist transcripts."""

    name = "transcription"

    def __init__(self, model_size: str = "small") -> None:
        self.engine = WhisperTranscriber(model_size=model_size)

    def initialize(self) -> Dict[str, str]:
        return {"status": "transcription subsystem initialized"}

    def transcribe_file(self, filepath: str, project_id: int) -> Dict[str, Any]:
        """
        Execute a transcription job for the given file and emit events downstream.
        """
        try:
            segments = self.engine.transcribe(filepath)
            normalized = normalize_segments(segments)

            out_dir = os.path.join("storage", "projects", str(project_id), "transcripts")
            os.makedirs(out_dir, exist_ok=True)

            output_path = os.path.join(out_dir, f"{os.path.basename(filepath)}.json")
            with open(output_path, "w", encoding="utf-8") as file_handle:
                json.dump(normalized, file_handle, indent=2)

            result = {
                "filepath": filepath,
                "project_id": project_id,
                "transcript": normalized,
                "output_path": output_path,
            }
            event_bus.publish("transcription_complete", result)
            return result
        except Exception as exc:  # pylint: disable=broad-except
            return {"error": str(exc), "filepath": filepath, "project_id": project_id}

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}


registry.register_subsystem("transcription", TranscriptionSubsystem())
