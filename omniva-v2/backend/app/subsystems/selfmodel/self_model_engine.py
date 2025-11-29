"""Global self-model maintaining coherent agent identity."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/selfmodel/self_model_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/selfmodel/self_model_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/selfmodel/self_model_engine with cognitive telemetry.


from __future__ import annotations

from collections import Counter
from datetime import datetime
from statistics import mean
from typing import Any, Dict, List, Optional


class SelfModelEngine:
    """
    Maintains global agent identity:
      - agent traits
      - temperament baseline
      - emotional baseline
      - drift + resilience profile
      - federated global signals
      - constellation consensus influence
    """

    DEFAULT_SELF: Dict[str, Any] = {
        "agent_name": "Omniva",
        "version": "2.0",
        "temperament": "analytic",
        "persona_anchor": "analytic",
        "confidence": 0.5,
        "resilience": 0.5,
        "exploration_bias": 0.5,
        "drift": 0.0,
        "global_emotion": 0.5,
        "global_trend": 0.0,
        "constellation_consensus": 0.0,
    }

    def __init__(self, registry, rules) -> None:
        self.registry = registry
        self.rules = rules
        self.state: Dict[str, Any] = dict(self.DEFAULT_SELF)
        self.history: List[Dict[str, Any]] = []
        self.lore_log: List[Dict[str, Any]] = []

    def _subsystem(self, name: str) -> Optional[Any]:
        return self.registry.get_subsystem(name) or getattr(self.registry, name, None)

    def _project_ids(self) -> List[int]:
        projects = self._subsystem("project_manager") or self._subsystem("projects")
        if projects and hasattr(projects, "get_all_project_ids"):
            try:
                return list(projects.get_all_project_ids())
            except Exception:  # pragma: no cover - defensive fallback
                return []
        return []

    def _record_history(self, avg_stress: float, avg_drift: float, consensus: float) -> None:
        snapshot = {
            "timestamp": datetime.utcnow().isoformat(),
            "temperament": self.state.get("temperament"),
            "confidence": self.state.get("confidence"),
            "resilience": self.state.get("resilience"),
            "exploration_bias": self.state.get("exploration_bias"),
            "drift": self.state.get("drift"),
            "avg_stress": avg_stress,
            "avg_drift": avg_drift,
            "consensus": consensus,
        }
        self.history.append(snapshot)
        if len(self.history) > 50:
            self.history = self.history[-50:]

    def recompute_identity(self) -> Dict[str, Any]:
        intel = self._subsystem("intelligence")
        project_ids = self._project_ids()
        if not intel or not project_ids:
            return dict(self.state)

        fed = self._subsystem("federation")
        constellation = self._subsystem("constellation")

        stresses: List[float] = []
        drifts: List[float] = []
        personas: List[str] = []

        for pid in project_ids:
            if hasattr(intel, "emotion_model"):
                emos = intel.emotion_model.get(pid)
                stresses.append(emos.get("stress", 0.3))
            if hasattr(intel, "cognition"):
                drift_state = intel.cognition.drift.get(pid)
                drifts.append(drift_state.get("drift_strength", 0.0))
            if hasattr(intel, "persona"):
                persona = intel.persona.get_persona(pid)
                personas.append(persona.get("temperament", "calm"))

        avg_stress = mean(stresses) if stresses else 0.3
        avg_drift = mean(drifts) if drifts else self.state.get("drift", 0.0)
        persona_anchor = Counter(personas).most_common(1)[0][0] if personas else self.state["temperament"]

        heuristics = fed.shared_heuristics if fed else {}
        global_emotion = heuristics.get("global_emotion_baseline", self.state.get("global_emotion", 0.5))
        global_trend = heuristics.get("global_trend", self.state.get("global_trend", 0.0))

        constellation_links = constellation.cross_project_cooperation() if constellation else []
        consensus_strength = min(1.0, len(constellation_links) / 10.0)

        normalized_temperament = self.rules.normalize_temperament(
            persona_anchor,
            avg_stress,
            global_emotion,
        )

        exploration_base = 0.5 + (global_emotion - 0.5) * 0.6 - avg_drift * 0.2

        self.state.update(
            {
                "temperament": normalized_temperament,
                "persona_anchor": persona_anchor,
                "drift": round(avg_drift, 4),
                "confidence": round(max(0.1, 1.0 - avg_stress), 4),
                "resilience": round(min(1.0, 0.4 + (1 - avg_drift) * 0.5), 4),
                "exploration_bias": round(min(1.0, max(0.1, exploration_base)), 4),
                "global_emotion": round(global_emotion, 4),
                "global_trend": round(global_trend, 4),
                "constellation_consensus": round(consensus_strength, 4),
            }
        )

        self.state = self.rules.normalize_identity_traits(self.state)
        self._record_history(avg_stress, avg_drift, consensus_strength)
        return dict(self.state)

    def record_lore_entry(self, entry: Dict[str, Any]) -> None:
        """
        Store symbolic lore snapshots coming from the Soul Bind engine.
        """
        self.lore_log.append(entry)
        if len(self.lore_log) > 100:
            self.lore_log = self.lore_log[-100:]

    def get_identity(self) -> Dict[str, Any]:
        return {
            "state": dict(self.state),
            "history": list(self.history),
            "lore": self.lore_log[-20:],
        }
