"""Emotional feedback engine for affect-based modulation."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/intelligence/emotion/emotional_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/emotion/emotional_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/emotion/emotional_engine with cognitive telemetry.


from __future__ import annotations

from typing import Dict, List

from .emotion_model import EmotionModel


class EmotionalEngine:
    """Update emotions and apply affect-weighted adjustments."""

    def __init__(self, model: EmotionModel) -> None:
        self.model = model

    def compute(self, project_id: int, ctx: Dict) -> Dict:
        return self.model.update(project_id, ctx)

    def influence_priority(self, project_id: int, clips: List[Dict]) -> List[Dict]:
        if not clips:
            return []
        state = self.model.get(project_id)
        influenced: List[Dict] = []
        for clip in clips:
            trending = float(clip.get("trending", 0.0))
            semantic = float(clip.get("semantic", 0.0))
            priority = float(clip.get("priority", 0.0))
            affect_bonus = (
                state["excitement"] * trending
                + state["curiosity"] * (1 - semantic)
                + state["stability"] * semantic
                - state["stress"] * 0.2
                + state["confidence"] * 0.1
            )
            clone = dict(clip)
            clone["priority"] = round(priority + affect_bonus, 6)
            clone["emotion_bonus"] = round(affect_bonus, 6)
            influenced.append(clone)
        influenced.sort(key=lambda entry: entry.get("priority", 0.0), reverse=True)
        return influenced
