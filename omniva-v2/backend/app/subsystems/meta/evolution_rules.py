"""Deterministic evolution rules for strategic meta-learning."""

from __future__ import annotations

from typing import Dict


class EvolutionRules:
    """Collection of rule-based adjustments for project/global policies."""

    def adjust_posting_limits(self, project_data: Dict[str, float], policy: Dict) -> Dict:
        avg_trend = project_data.get("avg_trend", 0.0)
        avg_drift = project_data.get("avg_drift", 0.0)
        avg_stress = project_data.get("avg_stress", 0.0)

        if avg_trend > 0.6 and avg_stress < 0.4:
            policy["max_daily_posts"] = min(policy.get("max_daily_posts", 3) + 1, 10)
        if avg_drift > 0.5 or avg_stress > 0.6:
            policy["max_daily_posts"] = max(policy.get("max_daily_posts", 3) - 1, 1)
        return policy

    def adjust_temperament_weights(self, persona: Dict) -> Dict:
        temperament = persona.get("temperament")
        stress = persona.get("stress_baseline", 0.0)
        stagnation = persona.get("semantic_stagnation", 0.0)

        if stress > 0.6 and temperament == "aggressive":
            persona["temperament"] = "analytical"
        if stagnation > 0.5 and temperament in {"analytical", "calm"}:
            persona["temperament"] = "playful"
        return persona

    def adjust_federated_coefficients(self, global_stats: Dict) -> Dict:
        drift = global_stats.get("global_drift_baseline", 0.0)
        emotion = global_stats.get("global_emotion_baseline", 0.0)
        return {
            "semantic_weight": 1.0 + emotion * 0.3,
            "drift_penalty": max(0.1, 1.0 - drift),
            "trend_bonus": emotion * 0.2,
        }
