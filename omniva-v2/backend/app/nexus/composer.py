"""Composability layer for multi-subsystem snapshots."""

from __future__ import annotations

from typing import Any, Dict, Optional


class Composer:
    """
    High-level composition of multiple subsystem outputs into unified payloads.
    """

    def __init__(self, registry) -> None:
        self.registry = registry

    def _subsystem(self, name: str) -> Optional[Any]:
        return self.registry.get_subsystem(name) or getattr(self.registry, name, None)

    def full_system_snapshot(self) -> Dict[str, Any]:
        """
        Composes:
          - identity
          - insights
          - archive summary
          - strategy map
          - constellation consensus
          - governance status
        """
        identity_engine = self._subsystem("selfmodel")
        observatory = self._subsystem("observatory")
        archive = self._subsystem("archive")
        strategy = self._subsystem("strategy")
        constellation = self._subsystem("constellation")
        governance = self._subsystem("governance")

        identity = identity_engine.get_identity() if identity_engine else {}
        insights = observatory.gather() if observatory else {}
        archive_summary = archive.summary() if archive and hasattr(archive, "summary") else {}
        strategy_map = strategy.global_emergent_map() if strategy and hasattr(strategy, "global_emergent_map") else {}
        constellation_view = constellation.consensus() if constellation and hasattr(constellation, "consensus") else {}
        governance_snapshot = governance.snapshot() if governance and hasattr(governance, "snapshot") else {}

        return {
            "identity": identity,
            "insights": insights,
            "archive": archive_summary,
            "strategy": strategy_map,
            "constellation": constellation_view,
            "governance": governance_snapshot,
        }

    def project_brief(self, project_id: int) -> Dict[str, Any]:
        """
        One-stop project-level composite view:
          - emotional state
          - drift state
          - strategy recommendation
          - discovery hints
          - posting time suggestion
        """
        intel = self._subsystem("intelligence")
        strategy = self._subsystem("strategy")
        scheduler = self._subsystem("scheduler")
        discovery = self._subsystem("discovery")

        emotion = intel.emotion_model.get(project_id) if intel and hasattr(intel, "emotion_model") else {}
        drift = intel.cognition.drift.get(project_id) if intel and hasattr(intel, "cognition") else {}
        strat = strategy.generate_for_project(project_id) if strategy and hasattr(strategy, "generate_for_project") else {}

        posting = None
        if scheduler and hasattr(scheduler, "suggest_post_time"):
            posting = scheduler.suggest_post_time(project_id)
        elif intel and hasattr(intel, "choose_posting_time"):
            posting = intel.choose_posting_time(project_id)
        else:
            posting = {"message": "scheduler unavailable"}

        new_posts = []
        if discovery:
            if hasattr(discovery, "check_new_posts"):
                new_posts = discovery.check_new_posts(project_id)
            elif hasattr(discovery, "discover_new_posts"):
                new_posts = discovery.discover_new_posts(project_id)

        return {
            "project_id": project_id,
            "emotion": emotion,
            "drift": drift,
            "strategy": strat,
            "posting_time": posting,
            "new_posts": new_posts,
        }
