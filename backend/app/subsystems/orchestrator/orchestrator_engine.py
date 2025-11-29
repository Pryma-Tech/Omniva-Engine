"""Master orchestrator for system-wide coordination."""

from __future__ import annotations

from typing import Dict


class MasterOrchestrator:
    """Coordinate global cycles and autonomy lifecycle."""

    def __init__(self, registry, health_checks) -> None:
        self.registry = registry
        self.health = health_checks

    def start_all(self) -> Dict[str, str]:
        projects = self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")
        autonomy = self.registry.autonomy
        if not projects:
            return {"status": "no_projects"}
        for pid in projects.get_all_project_ids():
            autonomy.start_project(pid)
        return {"status": "all_projects_started"}

    def stop_all(self) -> Dict[str, str]:
        projects = self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")
        autonomy = self.registry.autonomy
        if not projects:
            return {"status": "no_projects"}
        for pid in projects.get_all_project_ids():
            autonomy.stop_project(pid)
        return {"status": "all_projects_stopped"}

    def global_cycle(self) -> Dict:
        federation = self.registry.get_subsystem("federation")
        meta = self.registry.get_subsystem("meta")
        governance = self.registry.get_subsystem("governance")
        projects = self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")
        if federation and projects:
            for pid in projects.get_all_project_ids():
                federation.update_project_stats(pid)
            federation.federated_update()
        if meta:
            meta.run_cycle()
        governance_snapshot = {}
        if governance and projects:
            governance_snapshot = {
                pid: governance.policy_model.get_policy(pid) for pid in projects.get_all_project_ids()
            }
        health_report = self.health.system_health()
        return {
            "federation": federation.shared_heuristics if federation else {},
            "governance": governance_snapshot,
            "health": health_report,
        }
*** End Patch
