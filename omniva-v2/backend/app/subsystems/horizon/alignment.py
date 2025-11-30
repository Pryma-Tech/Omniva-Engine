"""Purpose alignment heuristics for Omniva Horizon."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/horizon/alignment.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/horizon/alignment with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/horizon/alignment with cognitive telemetry.


from __future__ import annotations

from typing import Dict

from .goal_model import HorizonGoalModel


class HorizonAlignmentEngine:
    """Measures and updates vision alignment across subsystems."""

    def __init__(self, registry, goals: HorizonGoalModel) -> None:
        self.registry = registry
        self.goals = goals

    def measure_alignment(self) -> Dict[str, object]:
        paradox_snapshot = self.registry.paradox.paradox_snapshot()
        infinity_snapshot = self.registry.infinity.infinity_snapshot()
        project_anomalies = paradox_snapshot.get("project_anomalies", {})
        anomaly_count = sum(len(anoms) for anoms in project_anomalies.values())
        stability = max(0.0, 1.0 - min(1.0, anomaly_count / max(len(project_anomalies) or 1, 1)))
        load_score = infinity_snapshot.get("load_score", 0.5)
        scaling_health = max(0.0, 1.0 - abs(load_score - 0.5) * 2)
        vision = self.goals.get_vision_vector()
        score = (
            stability * vision.get("sustain_system_stability", 0.3)
            + scaling_health * vision.get("minimize_failure_risk", 0.1)
        )
        return {"alignment_score": round(min(max(score, 0.0), 1.0), 4), "vision": vision}

    def update_goal_bias(self, new_weights: Dict[str, float]) -> Dict[str, float]:
        self.goals.global_vision.update(new_weights)
        return self.goals.get_vision_vector()
