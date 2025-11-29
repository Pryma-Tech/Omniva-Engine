"""Master orchestrator for system-wide coordination."""

from __future__ import annotations

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class MasterOrchestrator:
    """Coordinate global cycles and autonomy lifecycle."""

    def __init__(self, registry, health_checks) -> None:
        self.registry = registry
        self.health = health_checks

    def _projects(self):
        return self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")

    def _strategy_engine(self):
        return getattr(self.registry, "strategy", None) or self.registry.get_subsystem("strategy")

    def start_all(self) -> Dict[str, str]:
        projects = self._projects()
        autonomy = getattr(self.registry, "autonomy", None)
        if not projects or not autonomy:
            return {"status": "no_projects"}
        for pid in projects.get_all_project_ids():
            autonomy.start_project(pid)
        return {"status": "all_projects_started"}

    def stop_all(self) -> Dict[str, str]:
        projects = self._projects()
        autonomy = getattr(self.registry, "autonomy", None)
        if not projects or not autonomy:
            return {"status": "no_projects"}
        for pid in projects.get_all_project_ids():
            autonomy.stop_project(pid)
        return {"status": "all_projects_stopped"}

    def global_cycle(self) -> Dict[str, Any]:
        federation = self.registry.get_subsystem("federation") or getattr(self.registry, "federation", None)
        meta = self.registry.get_subsystem("meta") or getattr(self.registry, "meta", None)
        governance = self.registry.get_subsystem("governance") or getattr(self.registry, "governance", None)
        projects = self._projects()

        if federation and projects:
            for pid in projects.get_all_project_ids():
                federation.update_project_stats(pid)
            federation.federated_update()

        if meta:
            meta.run_cycle()

        strategies: Dict[int, Dict[str, Any]] = {}
        strategy_engine = self._strategy_engine()
        if strategy_engine and projects:
            for pid in projects.get_all_project_ids():
                try:
                    strategies[pid] = strategy_engine.generate_for_project(pid)
                except Exception as exc:  # pragma: no cover - defensive log
                    logger.warning("strategy generation failed for project %s: %s", pid, exc)

        identity_snapshot: Dict[str, Any] = {}
        if getattr(self.registry, "selfmodel", None):
            identity_snapshot = self.registry.selfmodel.recompute_identity()

        governance_snapshot = {}
        if governance and projects:
            governance_snapshot = {
                pid: governance.policy_model.get_policy(pid) for pid in projects.get_all_project_ids()
            }

        health_report = self.health.system_health()

        return {
            "federation": federation.shared_heuristics if federation else {},
            "governance": governance_snapshot,
            "strategies": strategies,
            "health": health_report,
            "identity": identity_snapshot,
        }
