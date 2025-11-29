"""Project-specific plan helpers for Omniva HTN planner."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/intelligence/planner/project_plans.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/planner/project_plans with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/planner/project_plans with cognitive telemetry.


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
