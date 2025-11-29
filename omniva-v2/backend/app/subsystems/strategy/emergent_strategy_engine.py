"""Emergent strategy engine that fuses federated and constellation signals."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/strategy/emergent_strategy_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/strategy/emergent_strategy_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/strategy/emergent_strategy_engine with cognitive telemetry.


from __future__ import annotations

from typing import Any, Dict, Optional


class EmergentStrategyEngine:
    """
    Generates emergent strategies across the entire Omniva constellation.
    Observes:
      - federated intelligence
      - constellation consensus
      - emotional & drift stability
      - trend flows
      - niche similarity clusters
    Produces:
      - novel themes
      - new tactics
      - cross-project collaborations
      - emergent strategy maps
    """

    def __init__(self, registry, rules) -> None:
        self.registry = registry
        self.rules = rules
        self.strategies: Dict[int, Dict[str, Any]] = {}

    def _subsystem(self, name: str) -> Optional[Any]:
        """
        Helper to access registry-managed subsystems whether or not they were
        explicitly registered via register_subsystem.
        """
        return self.registry.get_subsystem(name) or getattr(self.registry, name, None)

    def _trend_score(self, fed, project_id: int) -> float:
        if not fed:
            return 0.0
        return fed.trend_scores.get(project_id, 0.0)

    def _drift_strength(self, intel, project_id: int) -> float:
        if not intel or not hasattr(intel, "cognition"):
            return 0.0
        drift_state = intel.cognition.drift.get(project_id)
        return drift_state.get("drift_strength", 0.0)

    def _stress_level(self, intel, project_id: int) -> float:
        if not intel or not hasattr(intel, "emotion_model"):
            return 0.3
        emotion_state = intel.emotion_model.get(project_id)
        return emotion_state.get("stress", 0.3)

    def generate_for_project(self, project_id: int) -> Dict[str, Any]:
        fed = self._subsystem("federation")
        intel = self._subsystem("intelligence")
        constellation = self._subsystem("constellation")
        constellation_view = constellation.cross_project_cooperation() if constellation else []

        niche_sim = []
        if fed:
            niche_sim = list(fed.shared_heuristics.get("niche_similarity", []))
        elif constellation_view:
            # fall back to constellation cooperation map
            niche_sim = constellation_view

        trends = self._trend_score(fed, project_id)
        drift = self._drift_strength(intel, project_id)
        stress = self._stress_level(intel, project_id)

        theme = self.rules.synthesize_theme(niche_sim)
        tactic = self.rules.synthesize_posting_tactic(trends, drift, stress)
        collab = self.rules.propose_collab(niche_sim)

        result = {
            "project_id": project_id,
            "theme": theme,
            "tactic": tactic,
            "collaboration": collab,
            "signals": {
                "trend_score": trends,
                "drift_strength": drift,
                "stress": stress,
            },
            "constellation_consensus": constellation_view,
        }
        self.strategies[project_id] = result
        return result

    def global_emergent_map(self) -> Dict[str, Any]:
        """
        Produces a combined strategic map across the entire constellation.
        """
        fed = self._subsystem("federation")
        constellation = self._subsystem("constellation")
        similarities = []
        constellation_view = []
        if fed:
            similarities = list(fed.shared_heuristics.get("niche_similarity", []))
        if constellation:
            constellation_view = constellation.cross_project_cooperation()
            if not similarities:
                similarities = constellation_view

        return {
            "similarities": similarities,
            "strategies": self.strategies,
            "constellation": constellation_view,
        }

    def recommend_for_project(self, project_id: int) -> Dict[str, Any]:
        """
        Provide a lightweight recommendation summary for a project.
        """
        if project_id not in self.strategies:
            return self.generate_for_project(project_id)
        return self.strategies[project_id]

    def global_summary(self) -> Dict[str, Any]:
        return {
            "strategy_count": len(self.strategies),
            "last_entries": list(self.strategies.values())[-5:],
        }
