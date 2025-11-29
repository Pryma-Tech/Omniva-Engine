"""Synthetic affective state tracker."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/intelligence/emotion/emotion_model.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/emotion/emotion_model with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/emotion/emotion_model with cognitive telemetry.


from __future__ import annotations

from typing import Any, Dict


class EmotionModel:
    """Maintain per-project emotional state."""

    def __init__(self) -> None:
        self.state: Dict[int, Dict[str, Any]] = {}

    def get(self, project_id: int) -> Dict[str, Any]:
        if project_id not in self.state:
            self.state[project_id] = {
                "excitement": 0.5,
                "stress": 0.2,
                "curiosity": 0.5,
                "confidence": 0.5,
                "stability": 0.5,
                "history": [],
            }
        return self.state[project_id]

    def update(self, project_id: int, ctx: Dict[str, Any]) -> Dict[str, Any]:
        state = self.get(project_id)
        trend_score = ctx.get("trend_score", 0.5)
        drift_strength = ctx.get("drift_strength", 0.0)
        attention = ctx.get("attention", 1.0)
        temperament = ctx.get("temperament", "calm")

        bias_map = {
            "calm": {"stress": -0.1, "curiosity": -0.1},
            "analytic": {"stress": -0.05, "curiosity": 0.05},
            "analytical": {"stress": -0.05, "curiosity": 0.05},
            "energetic": {"excitement": 0.2, "curiosity": 0.1},
            "aggressive": {"stress": 0.2, "confidence": 0.1},
            "playful": {"curiosity": 0.2, "excitement": 0.1},
        }

        state["excitement"] += (trend_score - 0.5) * 0.5
        state["stress"] += drift_strength * 0.5
        state["curiosity"] += (1 - attention) * 0.2
        state["confidence"] += (attention - 1) * 0.3
        state["stability"] -= drift_strength * 0.3

        for key, delta in bias_map.get(temperament, {}).items():
            state[key] = state.get(key, 0.5) + delta

        for key in ["excitement", "stress", "curiosity", "confidence", "stability"]:
            state[key] = max(0.0, min(1.0, state[key]))

        snapshot = {k: state[k] for k in ["excitement", "stress", "curiosity", "confidence", "stability"]}
        state.setdefault("history", []).append(snapshot)
        self.state[project_id] = state
        return state

    def get_history(self, project_id: int, field: str) -> list[float]:
        """
        Retrieve historical values for a specific field.
        """
        state = self.get(project_id)
        history = state.get("history", [])
        return [entry.get(field, 0.0) for entry in history]
