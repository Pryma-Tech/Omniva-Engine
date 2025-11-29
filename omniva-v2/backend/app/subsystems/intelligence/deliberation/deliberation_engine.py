"""Agent deliberation engine for internal reasoning."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/intelligence/deliberation/deliberation_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/deliberation/deliberation_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/deliberation/deliberation_engine with cognitive telemetry.


from __future__ import annotations

import random
from datetime import datetime
from typing import Dict, List

from app.core import registry as global_registry


class DeliberationEngine:
    """Runs the reasoning fiber across subsystems."""

    def __init__(self, registry):
        self.registry = registry

    def deliberate(self, project_id: int, scored_clips: List[Dict]) -> Dict[str, Dict]:
        intel = self.registry.get_subsystem("intelligence")
        if intel is None:
            raise RuntimeError("Intelligence subsystem not registered")

        persona = intel.persona.get_persona(project_id)
        temperament = persona.get("temperament", "calm")
        voice = persona.get("voice", "minimal")

        framing = {
            "step": "framing",
            "time": datetime.utcnow().isoformat(),
            "context": {
                "clip_count": len(scored_clips),
                "temperament": temperament,
                "voice": voice,
                "attention": intel.cognition.attention.get(project_id, 1.0),
            },
        }

        modulated = intel.persona.apply_temperament(project_id, scored_clips)

        plan = intel.plan(project_id, goal="improve_growth")
        planner_step = {"step": "planner", "plan": plan.get("plan", []), "context": plan.get("context", {})}

        cog_state = intel.cognition.update_focus(
            project_id,
            temperament,
            trend_score=plan["context"].get("trend_score", 0.0),
            drift_detected=plan["context"].get("drift_detected", False),
        )

        emotion_state = intel.emotion_model.get(project_id)
        emotion_step = {"step": "emotion", "state": emotion_state}

        voted = intel.persona.committee_vote(project_id, modulated)
        committee_step = {"step": "committee_vote", "votes": voted[:5]}

        final_choice = voted[0] if voted else None
        base_confidence = random.uniform(0.5, 1.0)
        affect_shift = (emotion_state.get("confidence", 0.5) - emotion_state.get("stress", 0.2)) * 0.3
        confidence = round(max(0.1, min(1.0, base_confidence + affect_shift)), 3)
        final_summary = {
            "step": "final",
            "chosen_clip": final_choice,
            "confidence": confidence,
            "attention": cog_state["attention"],
            "reason": f"Selected using temperament={temperament}, plan_actions={len(plan.get('plan', []))}",
            "emotion": emotion_state,
        }

        for entry in (framing, emotion_step, planner_step, committee_step, final_summary):
            intel.cognition.push_memory(project_id, {"type": "deliberation", **entry})

        return {
            "framing": framing,
            "emotion": emotion_step,
            "planner": planner_step,
            "cognitive": cog_state,
            "committee": committee_step,
            "final": final_summary,
        }
