"""
Whisper transcription helpers.
"""

import os
from typing import List, Dict, Any

import whisper_timestamped as whisper


class WhisperTranscriber:
    """Wrapper around whisper-timestamped with configurable model size."""

    def __init__(self, model_size: str = "small") -> None:
        self.model = whisper.load_model(model_size)

    def transcribe(self, filepath: str) -> List[Dict[str, Any]]:
        """Run transcription and return the raw segments."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        result = whisper.transcribe(self.model, filepath)
        segments = result.get("segments", [])
        return segments
