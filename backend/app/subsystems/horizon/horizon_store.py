"""Lightweight horizon goal storage.

This is a simplified stand-in for the full omniva-v2 HorizonEngine:
it tracks per-project epoch goals and exposes a small vision snapshot.
"""

from __future__ import annotations

from typing import Any, Dict


class HorizonStore:
    """In-memory store for per-project epoch goals."""

    def __init__(self) -> None:
        self._goals: Dict[int, Dict[str, Any]] = {}

    def set_epoch_goal(self, project_id: int, goals: Dict[str, Any]) -> Dict[str, Any]:
        self._goals[project_id] = dict(goals or {})
        return {"project_id": project_id, "goals": self._goals[project_id]}

    def get_epoch_goal(self, project_id: int) -> Dict[str, Any]:
        return {"project_id": project_id, "goals": self._goals.get(project_id, {})}

    def vision(self) -> Dict[str, Any]:
        """Return a coarse snapshot of horizon goals across projects."""
        return {
            "projects": len(self._goals),
            "projects_with_goals": [pid for pid, goals in self._goals.items() if goals],
        }

