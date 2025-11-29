"""Main foresight module for Omniva Oracle."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/oracle/oracle_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/oracle/oracle_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/oracle/oracle_engine with cognitive telemetry.


from __future__ import annotations

from typing import Dict, List


class OracleEngine:
    """
    Combines:
      - forecasting engine
      - resonance engine
      - registry data streams
      - multi-horizon simulation
    """

    def __init__(self, registry, forecasting, resonance) -> None:
        self.registry = registry
        self.forecasting = forecasting
        self.resonance = resonance

    def _project_ids(self) -> List[int]:
        projects = (
            self.registry.get_subsystem("project_manager")
            or self.registry.get_subsystem("projects")
            or getattr(self.registry, "projects", None)
        )
        if projects and hasattr(projects, "get_all_project_ids"):
            return list(projects.get_all_project_ids())
        return []

    def project_forecast(self, project_id: int) -> Dict[str, dict]:
        intel = self.registry.get_subsystem("intelligence")
        fed = self.registry.get_subsystem("federation")

        stress_hist: List[float] = []
        drift_hist: List[float] = []
        trend_hist: List[float] = []

        if intel and hasattr(intel, "emotion_model") and hasattr(intel.emotion_model, "get_history"):
            stress_hist = intel.emotion_model.get_history(project_id, "stress")[-10:]
        if intel and hasattr(intel, "cognition") and hasattr(intel.cognition.drift, "get_history"):
            drift_hist = intel.cognition.drift.get_history(project_id)[-10:]
        if fed and hasattr(fed, "get_trend_history"):
            trend_hist = fed.get_trend_history(project_id)[-10:]

        return {
            "project_id": project_id,
            "trend": self.forecasting.forecast_trend(trend_hist),
            "stress": self.forecasting.forecast_stress(stress_hist),
            "drift": self.forecasting.forecast_drift(drift_hist),
        }

    def global_resonance(self) -> List[dict]:
        fed = self.registry.get_subsystem("federation")
        if not fed:
            return []
        similarity_pairs = fed.shared_heuristics.get("niche_similarity", []) if fed.shared_heuristics else []
        return self.resonance.predict_resonance(similarity_pairs)

    def foresight_snapshot(self) -> Dict[str, object]:
        """
        Full oracle snapshot combining:
          - forecasts for all projects
          - resonance mapping
          - current epoch
          - identity trending
        """
        forecasts = {pid: self.project_forecast(pid) for pid in self._project_ids()}
        return {
            "forecasts": forecasts,
            "resonance": self.global_resonance(),
            "epoch": self.registry.archive.current_epoch,
            "identity": self.registry.selfmodel.get_identity(),
        }

    def system_summary(self) -> Dict[str, float]:
        """
        Provide aggregate drift/stress/trend metrics used by Chorus/Horizon layers.
        """
        project_ids = self._project_ids()
        if not project_ids:
            return {"drift": 0.2, "stress": 0.3, "trend": 0.4}
        drifts: List[float] = []
        stresses: List[float] = []
        trends: List[float] = []
        for pid in project_ids:
            forecast = self.project_forecast(pid)
            drifts.append(forecast["drift"]["expected"])
            stresses.append(forecast["stress"]["expected"])
            trends.append(forecast["trend"]["expected"])
        avg = lambda values: sum(values) / max(len(values), 1)
        return {
            "drift": round(avg(drifts), 4),
            "stress": round(avg(stresses), 4),
            "trend": round(avg(trends), 4),
        }
