"""Global health diagnostics for Omniva orchestration."""

from __future__ import annotations

from statistics import mean
from typing import Any, Dict, List


class HealthChecks:
    """Compute per-project and global health summaries."""

    def __init__(self, registry) -> None:
        self.registry = registry

    def system_health(self) -> Dict[str, Any]:
        # TODO(omniva-v0.2): Persist health summaries to Stardust for time-series analysis.
        # TODO(omniva-v0.3): Trigger Eclipse remediation when stress/drift exceed thresholds.
        intel = self.registry.get_subsystem("intelligence")
        fed = self.registry.get_subsystem("federation")
        crisis = self.registry.get_subsystem("crisis")
        governance = self.registry.get_subsystem("governance")
        projects = self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")
        autonomy = getattr(self.registry, "autonomy", None)
        scheduler = self.registry.get_subsystem("scheduler")
        report: Dict[str, Any] = {"projects": {}, "global": {}}
        if not intel or not projects:
            return report

        all_drift: List[float] = []
        all_stress: List[float] = []
        running, paused = 0, 0

        for pid in projects.get_all_project_ids():
            drift = intel.cognition.drift.get(pid)
            emotion = intel.emotion_model.get(pid) if hasattr(intel, "emotion_model") else {}
            crises = crisis.get_crises(pid) if crisis else []
            policy = governance.policy_model.get_policy(pid) if governance else {}
            queue_depth = len(intel.cognition.recent_memory(pid))
            schedule = scheduler.get_project_schedule(pid) if scheduler else {}
            state = "idle"
            if autonomy and autonomy.is_running(pid):
                state = "running"
                running += 1
            elif autonomy and autonomy.paused.get(pid):
                state = "paused"
                paused += 1
            stress = emotion.get("stress", 0.2)
            drift_strength = drift.get("drift_strength", 0.0)
            all_drift.append(drift_strength)
            all_stress.append(stress)
            report["projects"][pid] = {
                "stress": stress,
                "drift": drift_strength,
                "crisis_count": len(crises),
                "daily_limit": policy.get("posting_limit"),
                "recent_memory_len": queue_depth,
                "worker_state": state,
                "schedule": schedule,
            }

        report["global"] = {
            "avg_drift": mean(all_drift) if all_drift else 0.0,
            "avg_stress": mean(all_stress) if all_stress else 0.0,
            "federated": fed.shared_heuristics if fed else {},
            "running_projects": running,
            "paused_projects": paused,
        }
        report["global"]["stable"] = (
            report["global"]["avg_stress"] < 0.65 and report["global"]["avg_drift"] < 0.65
        )
        return report
