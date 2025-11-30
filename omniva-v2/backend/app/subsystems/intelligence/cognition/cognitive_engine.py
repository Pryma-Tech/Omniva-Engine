"""Cognitive state engine tracking attention, working memory, and focus drift."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/intelligence/cognition/cognitive_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/cognition/cognitive_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/cognition/cognitive_engine with cognitive telemetry.


from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from .working_memory import WorkingMemory
from .drift_model import FocusDrift


class CognitiveEngine:
    """Manage per-project cognitive resources."""

    def __init__(self) -> None:
        self.attention: Dict[int, float] = {}
        self.memory: Dict[int, WorkingMemory] = {}
        self.drift = FocusDrift()

    def init_project(self, project_id: int) -> None:
        self.memory.setdefault(project_id, WorkingMemory())
        self.attention.setdefault(project_id, 1.0)

    def set_attention(self, project_id: int, value: float) -> float:
        self.init_project(project_id)
        clamped = max(0.1, min(value, 2.0))
        self.attention[project_id] = clamped
        return clamped

    def adjust_attention(self, project_id: int, drift_strength: float) -> float:
        self.init_project(project_id)
        current = self.attention[project_id]
        delta = (drift_strength - 0.05) * 0.2
        new_val = max(0.1, min(2.0, current - delta))
        self.attention[project_id] = new_val
        return new_val

    def push_memory(self, project_id: int, event: Dict[str, Any]) -> None:
        self.init_project(project_id)
        payload = {"timestamp": datetime.utcnow().isoformat(), **event}
        self.memory[project_id].push(payload)

    def recent_memory(self, project_id: int, count: int = 5):
        if project_id not in self.memory:
            return []
        return self.memory[project_id].recent(count)

    def update_focus(self, project_id: int, temperament: str, trend_score: float, drift_detected: bool) -> Dict[str, Any]:
        self.init_project(project_id)
        drift_state = self.drift.update(project_id, temperament, trend_score, drift_detected)
        attention = self.adjust_attention(project_id, drift_state["drift_strength"])
        payload = {"type": "focus_update", "drift": drift_state, "attention": attention}
        self.push_memory(project_id, payload)
        return payload
