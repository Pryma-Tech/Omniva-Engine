"""Planner engine that builds HTN plans using Omniva context signals."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from app.core.registry import registry

from .htn_core import HTNPlanner
from .project_plans import DEFAULT_GOALS, default_goal_for_project
from .task_library import build_task_library


class PlannerEngine:
    """Builds planning context and runs the HTN planner."""

    def __init__(self) -> None:
        tasks, methods = build_task_library()
        self.planner = HTNPlanner(tasks=tasks, methods=methods)

    def _intel(self):
        intel = registry.get_subsystem("intelligence")
        if intel is None:
            raise RuntimeError("Intelligence subsystem not registered")
        return intel

    def build_context(self, project_id: int) -> Dict[str, Any]:
        intel = self._intel()
        personality = intel.personality.get_personality(project_id)
        personality_key = personality.get("key", "balanced")
        persona_profile = intel.persona.get_persona(project_id)
        temperament_meta = intel.persona.temperaments.get(persona_profile["temperament"], {})

        trending_map = intel.get_trending_keywords(project_id)
        total_trend_hits = sum(entry.get("count", 0) for entry in trending_map.values())
        trend_score = min(1.0, total_trend_hits / 50.0) if total_trend_hits else 0.0

        ltm = intel.ltm_report(project_id)
        drift_log = ltm.get("drift_log", [])
        drift_detected = bool(drift_log and drift_log[-1].get("drift_detected"))

        optimizer_history = intel.get_self_opt_history(project_id)
        optimizer_rounds = len(optimizer_history.get("rounds", [])) if optimizer_history else 0

        ctx = {
            "project_id": project_id,
            "personality": personality_key,
            "trend_score": trend_score,
            "drift_detected": drift_detected,
            "ltm_health": ltm.get("health", {}),
            "optimizer_rounds": optimizer_rounds,
            "persona": persona_profile,
            "temperament_tone": temperament_meta.get("tone"),
            "timestamp": datetime.utcnow().isoformat(),
        }
        return ctx

    def plan(self, project_id: int, goal: str | None = None) -> Dict[str, Any]:
        ctx = self.build_context(project_id)
        target_goal = goal or default_goal_for_project(ctx["personality"])
        if target_goal not in DEFAULT_GOALS:
            raise ValueError(f"Unsupported goal: {target_goal}")
        actions = self.planner.plan(target_goal, ctx)
        intel = self._intel()
        voice_summary = intel.persona.apply_voice(
            project_id,
            {"reason": f"Plan '{target_goal}' with {len(actions)} actions.", "score": len(actions)},
        )
        return {
            "project_id": project_id,
            "goal": target_goal,
            "context": ctx,
            "plan": actions,
            "voice_summary": voice_summary,
        }
