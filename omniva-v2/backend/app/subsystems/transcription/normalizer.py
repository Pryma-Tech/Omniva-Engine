"""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/transcription/normalizer.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/transcription/normalizer with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/transcription/normalizer with cognitive telemetry.

Utility helpers for parsing Whisper segments to Omniva's normalized format.
"""

from typing import Any, Dict, List


def normalize_segments(segments: List[Dict[str, Any]]) -> List[Dict[str, float]]:
    """
    Convert whisper segments into clean, standard Omniva format.
    """
    results: List[Dict[str, float]] = []
    for seg in segments:
        results.append(
            {
                "text": seg.get("text", "").strip(),
                "start": float(seg.get("start", 0)),
                "end": float(seg.get("end", 0)),
            }
        )
    return results
