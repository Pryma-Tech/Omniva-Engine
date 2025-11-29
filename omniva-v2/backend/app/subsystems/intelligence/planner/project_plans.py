"""Project-specific plan helpers for Omniva HTN planner."""

from __future__ import annotations

from typing import Dict

DEFAULT_GOALS = [
    "improve_growth",
    "recover_drift",
    "chase_trend",
    "increase_consistency",
]


def default_goal_for_project(personality_key: str) -> str:
    mapping: Dict[str, str] = {
        "viral_hunter": "chase_trend",
        "growth_spiral": "improve_growth",
        "brand_guardian": "increase_consistency",
    }
    return mapping.get(personality_key, "improve_growth")
