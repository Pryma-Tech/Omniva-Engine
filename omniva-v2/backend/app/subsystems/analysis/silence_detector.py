"""Simple heuristic for identifying low-content transcript segments."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/analysis/silence_detector.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/analysis/silence_detector with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/analysis/silence_detector with cognitive telemetry.


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
