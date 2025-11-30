"""Unified agent brain for final arbitration."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/intelligence/brain/brain_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/brain/brain_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/brain/brain_engine with cognitive telemetry.


from __future__ import annotations

from datetime import datetime
from typing import Dict, List


class UnifiedAgentBrain:
    """Collect and arbitrate signals across intelligence subsystems."""

    def __init__(self, registry) -> None:
        self.registry = registry

    def gather_signals(self, project_id: int, clips: List[Dict]) -> Dict[str, Dict]:
        intel = self.registry.get_subsystem("intelligence")
        if intel is None:
            raise RuntimeError("Intelligence subsystem not registered")

        sem = intel.semantic_rank(project_id, clips)
        kw = intel.keyword_ranker.rank(project_id, clips)
        audio = [{"clip_id": clip.get("id"), "audio_score": 0} for clip in clips]
        priorities = intel.prioritize_with_personality(project_id, sem, kw, audio)

        bt = intel.run_behavior_tree(project_id, {"project": {"id": project_id, "autonomous": True}})
        plan = intel.plan(project_id)
        deliberation = intel.deliberate(project_id, priorities)
        emotion = intel.emotion_model.get(project_id)
        cognition = {
            "attention": intel.cognition.attention.get(project_id, 1.0),
            "drift": intel.cognition.drift.get(project_id),
            "memory": intel.cognition.recent_memory(project_id, 5),
        }
        ltm = intel.ltm_report(project_id)
        federation = self.registry.get_subsystem("federation")
        federated = federation.share_to_project(project_id) if federation else {}

        constellation = self.registry.get_subsystem("constellation")
        collaboration = (
            constellation.collaborative_decision(project_id, {"signals": "preview"})
            if constellation
            else {"consensus": {}}
        )

        return {
            "priorities": priorities,
            "behavior_tree": bt,
            "planner": plan,
            "deliberation": deliberation,
            "emotion": emotion,
            "cognition": cognition,
            "ltm": ltm,
            "federated": federated,
            "constellation": collaboration.get("consensus", {}),
        }

    def arbitrate(self, project_id: int, signals: Dict[str, Dict]) -> Dict[str, Dict]:
        intel = self.registry.get_subsystem("intelligence")
        priorities = signals.get("priorities", [])
        emotion = signals.get("emotion", {})
        cognition = signals.get("cognition", {})
        plan = signals.get("planner", {}).get("plan", [])

        attention = cognition.get("attention", 1.0)
        drift_strength = cognition.get("drift", {}).get("drift_strength", 0.0)
        excitement = emotion.get("excitement", 0.5)
        stress = emotion.get("stress", 0.2)

        w_priorities = attention
        w_emotion = excitement + (1 - stress)
        w_planner = min(1.0, len(plan) / 4 + 0.5)
        w_stability = max(0.1, 1 - drift_strength)

        results = []
        for clip in priorities:
            base = clip.get("priority", 0.0)
            arb_score = (
                base * w_priorities
                + clip.get("trending", 0.0) * w_emotion
                + clip.get("semantic", 0.0) * w_stability
            )
            if "action:prioritize_trending_audio" in plan:
                arb_score += clip.get("trending", 0.0) * 0.2
            results.append({"clip_id": clip.get("clip_id"), "score": round(arb_score, 6), "base_priority": base})

        results.sort(key=lambda entry: entry.get("score", 0.0), reverse=True)
        final_choice = results[0] if results else None

        arbitration = {
            "final_choice": final_choice,
            "scores": results,
            "weights": {
                "priority": w_priorities,
                "emotion": w_emotion,
                "planner": w_planner,
                "stability": w_stability,
            },
        }

        if intel:
            intel.cognition.push_memory(
                project_id,
                {
                    "type": "brain_arbitration",
                    "arbitration": arbitration,
                    "timestamp": datetime.utcnow().isoformat(),
                },
            )
        return arbitration

    def decide(self, project_id: int, clips: List[Dict]) -> Dict[str, Dict]:
        signals = self.gather_signals(project_id, clips)
        arbitration = self.arbitrate(project_id, signals)
        safety = self.registry.get_subsystem("safety")
        if safety:
            ok, reason = safety.validate_action(project_id, arbitration)
            if not ok:
                crisis = self.registry.get_subsystem("crisis")
                if crisis:
                    crisis.handle_exception(project_id, "action_validation", Exception(reason), reason)
                return {"error": "action_rejected_by_safety", "reason": reason}
        decision = {
            "project_id": project_id,
            "time": datetime.utcnow().isoformat(),
            "chosen_clip": arbitration.get("final_choice"),
            "arbitration": arbitration,
            "signals": signals,
            "confidence": round(min(1.0, arbitration["weights"]["priority"] * 0.6 + 0.4), 3),
            "reason": "UnifiedAgentBrain combined all subsystem signals to reach this action.",
        }
        governance = self.registry.get_subsystem("governance")
        if governance:
            ok, reason = governance.enforce(project_id, decision)
            if not ok:
                crisis = self.registry.get_subsystem("crisis")
                if crisis:
                    crisis.handle_exception(project_id, "governance_rejection", Exception(reason), reason)
                return {"error": "decision_rejected_by_governance", "reason": reason}
        intel = self.registry.get_subsystem("intelligence")
        if intel:
            intel.cognition.push_memory(project_id, {"type": "brain_decision", **decision})
        return decision
