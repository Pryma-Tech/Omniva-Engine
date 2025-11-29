"""Focus drift calculations for the cognitive engine."""

from __future__ import annotations

import math
from typing import Any, Dict, List


def _default_state() -> Dict[str, Any]:
    return {"volatility": 0.0, "drift_strength": 0.0, "history": []}


class FocusDrift:
    """Track focus drift metrics per project."""

    def __init__(self) -> None:
        self.state: Dict[int, Dict[str, Any]] = {}

    def get(self, project_id: int) -> Dict[str, Any]:
        return self.state.get(project_id, _default_state())

    def update(self, project_id: int, temperament: str, trend_score: float, drift_detected: bool) -> Dict[str, Any]:
        base_map = {
            "calm": 0.01,
            "analytical": 0.02,
            "energetic": 0.05,
            "aggressive": 0.08,
            "playful": 0.1,
        }
        base_drift = base_map.get(temperament, 0.03)
        trend_influence = trend_score * 0.05
        drift_penalty = 0.1 if drift_detected else 0.0
        drift_strength = base_drift + trend_influence + drift_penalty

        state = self.get(project_id)
        state["drift_strength"] = drift_strength
        state["volatility"] = math.tanh(drift_strength * 2)
        state.setdefault("history", []).append(
            {
                "drift": drift_strength,
                "trend": trend_score,
                "detected": drift_detected,
            }
        )
        self.state[project_id] = state
        return state

    def get_history(self, project_id: int) -> List[float]:
        state = self.state.get(project_id)
        if not state:
            return []
        return [entry.get("drift", 0.0) for entry in state.get("history", [])]
