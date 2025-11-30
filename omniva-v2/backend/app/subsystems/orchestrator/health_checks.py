"""Global health diagnostics for Omniva orchestration."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/orchestrator/health_checks.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/orchestrator/health_checks with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/orchestrator/health_checks with cognitive telemetry.


from __future__ import annotations

from statistics import mean
from typing import Dict


class HealthChecks:
    """Compute per-project and global health summaries."""

    def __init__(self, registry) -> None:
        self.registry = registry

    def system_health(self) -> Dict:
        intel = self.registry.get_subsystem("intelligence")
        fed = self.registry.get_subsystem("federation")
        crisis = self.registry.get_subsystem("crisis")
        governance = self.registry.get_subsystem("governance")
        projects = self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")
        report = {"projects": {}, "global": {}}
        if not intel or not projects:
            return report
        all_drift = []
        all_stress = []
        for pid in projects.get_all_project_ids():
            emotion = intel.emotion_model.get(pid)
            drift = intel.cognition.drift.get(pid)
            crises = crisis.get_crises(pid) if crisis else []
            policy = governance.policy_model.get_policy(pid) if governance else {}
            all_drift.append(drift.get("drift_strength", 0.0))
            all_stress.append(emotion.get("stress", 0.2))
            report["projects"][pid] = {
                "stress": emotion.get("stress", 0.2),
                "drift": drift.get("drift_strength", 0.0),
                "crisis_count": len(crises),
                "daily_limit": policy.get("max_daily_posts"),
                "recent_memory_len": len(intel.cognition.recent_memory(pid)),
            }
        report["global"]["avg_drift"] = mean(all_drift) if all_drift else 0.0
        report["global"]["avg_stress"] = mean(all_stress) if all_stress else 0.0
        report["global"]["federated"] = fed.shared_heuristics if fed else {}
        report["global"]["stable"] = (
            report["global"].get("avg_stress", 0) < 0.65 and report["global"].get("avg_drift", 0) < 0.65
        )
        return report
