"""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/transcription/transcription_subsystem.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/transcription/transcription_subsystem with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/transcription/transcription_subsystem with cognitive telemetry.

Real transcription subsystem powered by Whisper.
"""

import asyncio
import json
import os
from typing import Any, Dict, List, Optional, Tuple

from app.core.event_bus import event_bus
from app.core.job_queue import job_queue
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

    def _infer_project_id(self, filepath: str) -> Optional[int]:
        parts = filepath.split(os.sep)
        if "projects" in parts:
            idx = parts.index("projects")
            if idx + 1 < len(parts):
                try:
                    return int(parts[idx + 1])
                except ValueError:
                    return None
        return None

    def _transcribe(self, filepath: str) -> Tuple[List[Dict[str, Any]], str]:
        segments = self.engine.transcribe(filepath)
        normalized = normalize_segments(segments)
        transcript_text = " ".join(seg.get("text", "") for seg in normalized).strip()
        return normalized, transcript_text

    async def transcribe(self, filepath: str, project_id: Optional[int] = None) -> str:
        """
        Async transcription used by the autonomous engine.
        """
        normalized, transcript_text = await asyncio.to_thread(self._transcribe, filepath)
        pid = project_id if project_id is not None else self._infer_project_id(filepath)

        if pid is not None:
            out_dir = os.path.join("storage", "projects", str(pid), "transcripts")
            os.makedirs(out_dir, exist_ok=True)
            output_path = os.path.join(out_dir, f"{os.path.basename(filepath)}.json")
            with open(output_path, "w", encoding="utf-8") as file_handle:
                json.dump(normalized, file_handle, indent=2)

        return transcript_text

    def transcribe_file(self, filepath: str, project_id: int) -> Dict[str, Any]:
        """
        Execute a transcription job for the given file and emit events downstream.
        """
        try:
            normalized, _ = self._transcribe(filepath)

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
            job_queue.enqueue(
                "analyze",
                {
                    "filepath": output_path,
                    "project_id": project_id,
                    "keywords": [],
                },
            )
            return result
        except Exception as exc:  # pylint: disable=broad-except
            return {"error": str(exc), "filepath": filepath, "project_id": project_id}

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}


registry.register_subsystem("transcription", TranscriptionSubsystem())
