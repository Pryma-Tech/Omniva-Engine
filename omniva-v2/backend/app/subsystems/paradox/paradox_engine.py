"""Temporal coherence guardian for Omniva Paradox."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/paradox/paradox_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/paradox/paradox_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/paradox/paradox_engine with cognitive telemetry.


from __future__ import annotations

from typing import Dict, List


class ParadoxEngine:
    """
    Oversees anomaly detection and reconciliation across Oracle, Astral, and Infinity.
    """

    def __init__(self, registry, rules, recon) -> None:
        self.registry = registry
        self.rules = rules
        self.recon = recon

    def _identity_state(self) -> Dict[str, float]:
        identity = self.registry.selfmodel.get_identity()
        state = identity.get("state", {})
        fallback = identity.get("drift", 0.0) if isinstance(identity, dict) else 0.0
        return state or {"drift": fallback}

    def _projects(self) -> List[int]:
        projects = (
            self.registry.get_subsystem("project_manager")
            or self.registry.get_subsystem("projects")
            or getattr(self.registry, "projects", None)
        )
        if projects and hasattr(projects, "get_all_project_ids"):
            return list(projects.get_all_project_ids())
        return []

    def check_project(self, project_id: int) -> List[str]:
        oracle = self.registry.oracle.project_forecast(project_id)
        drift_curr = oracle["drift"]["expected"]
        trend_curr = oracle["trend"]["expected"]
        prev_drift = self._identity_state().get("drift", drift_curr)

        anomalies: List[str] = []
        if self.rules.drift_spike(drift_curr, prev_drift):
            anomalies.append("drift_spike")
        if self.rules.negative_trend(trend_curr):
            anomalies.append("negative_trend")
        return anomalies

    def check_infinity(self) -> List[str]:
        inf = self.registry.infinity.infinity_snapshot()
        if self.rules.infinity_mismatch(inf["load_score"], inf["current_scale"]):
            return ["infinity_mismatch"]
        return []

    def check_astral(self, project_id: int) -> List[str]:
        branches = self.registry.astral.alternate_futures(project_id)["branches"]
        if self.rules.astral_divergence(branches):
            return ["astral_divergence"]
        return []

    def reconcile_project(self, project_id: int) -> Dict[str, object]:
        oracle = self.registry.oracle.project_forecast(project_id)
        drift_curr = oracle["drift"]["expected"]
        trend_curr = oracle["trend"]["expected"]
        prev_drift = self._identity_state().get("drift", drift_curr)
        repaired = {
            "drift": self.recon.reconcile_drift(drift_curr, prev_drift),
            "trend": self.recon.clamp_trend(trend_curr),
        }
        return {"project_id": project_id, "repaired": repaired}

    def reconcile_astral(self, project_id: int) -> Dict[str, object]:
        branches = self.registry.astral.alternate_futures(project_id)["branches"]
        return {"project_id": project_id, "branches": self.recon.collapse_branch(branches)}

    def reconcile_infinity(self) -> Dict[str, object]:
        inf = self.registry.infinity.infinity_snapshot()
        fixed_scale = self.recon.fix_scale(inf["load_score"], inf["current_scale"])
        return {"current_scale": inf["current_scale"], "patched_scale": fixed_scale}

    def paradox_snapshot(self) -> Dict[str, object]:
        projects = self._projects()
        project_anomalies = {pid: self.check_project(pid) for pid in projects}
        astral_anomalies = {pid: self.check_astral(pid) for pid in projects}
        infinity_anomalies = self.check_infinity()
        return {
            "project_anomalies": project_anomalies,
            "astral_anomalies": astral_anomalies,
            "infinity": infinity_anomalies,
            "epoch": self.registry.archive.current_epoch,
        }
