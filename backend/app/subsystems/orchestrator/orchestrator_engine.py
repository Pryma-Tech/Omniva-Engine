"""Master orchestrator for system-wide coordination."""

from __future__ import annotations

import time
from datetime import datetime
from typing import Dict, Iterable, List


class MasterOrchestrator:
    """Coordinate global cycles and autonomy lifecycle."""

    def __init__(self, registry, health_checks) -> None:
        self.registry = registry
        self.health = health_checks

    def start_all(self, project_ids: Iterable[int] | None = None) -> Dict[str, object]:
        projects = self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")
        autonomy = self.registry.autonomy
        if not projects or not autonomy:
            return {"status": "no_projects"}
        target_ids = self._select_projects(projects, project_ids)
        started: List[int] = []
        already_running: List[int] = []
        for pid in target_ids:
            if autonomy.is_running(pid):
                already_running.append(pid)
                continue
            result = autonomy.start_project(pid)
            if result.get("status") == "started":
                started.append(pid)
        status = "all_projects_started" if len(started) == len(target_ids) else "partial_start"
        return {"status": status, "started": started, "already_running": already_running}

    def stop_all(self, project_ids: Iterable[int] | None = None, *, drain: bool = True) -> Dict[str, object]:
        projects = self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")
        autonomy = self.registry.autonomy
        if not projects or not autonomy:
            return {"status": "no_projects"}
        target_ids = self._select_projects(projects, project_ids)
        drained: List[int] = []
        for pid in target_ids:
            if drain:
                self._drain_project(pid)
                drained.append(pid)
            autonomy.stop_project(pid)
        return {"status": "all_projects_stopped", "drained": drained, "stopped": target_ids}

    def global_cycle(self) -> Dict[str, object]:
        # TODO(omniva-v0.2): Integrate Horizon and Pantheon summaries into this report.
        # TODO(omniva-v0.3): Allow configurable hooks for custom governance policies.
        federation = self.registry.get_subsystem("federation")
        meta = self.registry.get_subsystem("meta")
        governance = self.registry.get_subsystem("governance")
        projects = self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")
        stages: Dict[str, float] = {}
        start_time = time.perf_counter()

        if federation and projects:
            for pid in projects.get_all_project_ids():
                federation.update_project_stats(pid)
            federation.federated_update()
        stages["federation"] = time.perf_counter() - start_time

        if meta:
            meta_start = time.perf_counter()
            meta.run_cycle()
            stages["meta"] = time.perf_counter() - meta_start

        governance_snapshot = {}
        if governance and projects:
            gov_start = time.perf_counter()
            governance_snapshot = {
                pid: governance.policy_model.get_policy(pid) for pid in projects.get_all_project_ids()
            }
            stages["governance_snapshot"] = time.perf_counter() - gov_start

        health_start = time.perf_counter()
        health_report = self.health.system_health()
        stages["health"] = time.perf_counter() - health_start

        return {
            "federation": federation.shared_heuristics if federation else {},
            "governance": governance_snapshot,
            "health": health_report,
            "metrics": {
                "stages_seconds": stages,
                "cycle_completed_at": datetime.utcnow().isoformat(),
            },
        }

    def _select_projects(self, projects, requested: Iterable[int] | None) -> List[int]:
        all_ids = projects.get_all_project_ids()
        if not requested:
            return all_ids
        requested_set = {int(pid) for pid in requested}
        return [pid for pid in all_ids if pid in requested_set]

    def _drain_project(self, project_id: int) -> None:
        intel = self.registry.get_subsystem("intelligence")
        if not intel:
            return
        schedule = self.registry.get_subsystem("scheduler")
        schedule_snapshot = schedule.get_project_schedule(project_id) if schedule else {}
        intel.cognition.push_memory(
            project_id,
            {
                "type": "orchestrator_drain",
                "timestamp": datetime.utcnow().isoformat(),
                "schedule": schedule_snapshot,
            },
        )
