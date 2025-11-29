"""Central analytics engine for the Omniva Observatory."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/observatory/observatory_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/observatory/observatory_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/observatory/observatory_engine with cognitive telemetry.


from __future__ import annotations

from typing import Any, Dict, List, Optional

from .metrics_calculator import MetricsCalculator


class ObservatoryEngine:
    """
    Central analytics engine combining:
      - emotional trends
      - drift motion
      - federated signals
      - constellation similarity
      - identity evolution
      - archival epochs
    """

    def __init__(self, registry, metrics: MetricsCalculator) -> None:
        self.registry = registry
        self.metrics = metrics

    def _get_subsystem(self, name: str) -> Optional[Any]:
        return self.registry.get_subsystem(name) or getattr(self.registry, name, None)

    def _project_ids(self) -> List[int]:
        projects = self._get_subsystem("project_manager") or self._get_subsystem("projects")
        if projects and hasattr(projects, "get_all_project_ids"):
            try:
                return list(projects.get_all_project_ids())
            except Exception:  # pragma: no cover - defensive guard
                return []
        return []

    def _project_states(self) -> List[Dict[str, float]]:
        intel = self._get_subsystem("intelligence")
        if not intel:
            return []
        states: List[Dict[str, float]] = []
        for project_id in self._project_ids():
            emotion = intel.emotion_model.get(project_id) if hasattr(intel, "emotion_model") else {}
            drift_state = intel.cognition.drift.get(project_id) if hasattr(intel, "cognition") else {}
            states.append(
                {
                    "project_id": project_id,
                    "stress": float(emotion.get("stress", 0.0)),
                    "drift": float(drift_state.get("drift_strength", 0.0)),
                }
            )
        return states

    def gather(self) -> Dict[str, Any]:
        federation = self._get_subsystem("federation")
        archive = self._get_subsystem("archive")
        identity_engine = self._get_subsystem("selfmodel")
        constellation = self._get_subsystem("constellation")

        project_states = self._project_states()
        trend_scores = federation.trend_scores.values() if federation and federation.trend_scores else []
        heuristics = federation.shared_heuristics if federation else {}
        similarities = heuristics.get("niche_similarity", [])
        identity = identity_engine.get_identity() if identity_engine else {}
        epoch = getattr(archive, "current_epoch", "unknown")
        event_count = len(getattr(archive, "timeline", []) or [])
        constellation_links = (
            constellation.cross_project_cooperation() if constellation else heuristics.get("niche_similarity", [])
        )

        return {
            "emotional": self.metrics.emotional_metrics(project_states),
            "drift": self.metrics.drift_metrics(project_states),
            "trends": self.metrics.trend_metrics(list(trend_scores)),
            "similarity": self.metrics.constellation_summary(similarities),
            "identity": identity,
            "constellation": {"links": constellation_links},
            "epoch": epoch,
            "event_count": event_count,
        }
