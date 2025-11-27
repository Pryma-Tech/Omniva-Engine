"""Simple heuristic for identifying low-content transcript segments."""

from typing import List


def detect_silence(segments: List[dict]) -> List[bool]:
    """
    Returns a list of booleans marking low-energy segments.
    Uses text length as a lightweight stand-in for amplitude analysis.
    """
    silence_flags: List[bool] = []
    for segment in segments:
        text = segment.get("text", "").strip()
        silence_flags.append(len(text) < 3)
    return silence_flags
