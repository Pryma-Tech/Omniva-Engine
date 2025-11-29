"""Global scheduled tasks triggered by the Heartbeat engine."""

from __future__ import annotations

from datetime import datetime
from typing import Dict


class CronTasks:
    """Define global tasks executed on a schedule."""

    def __init__(self, registry) -> None:
        self.registry = registry

    def _projects(self):
        return self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")

    async def run_daily_midnight_reset(self) -> Dict[str, str]:
        intel = self.registry.get_subsystem("intelligence")
        projects = self._projects()
        if not intel or not projects:
            return {"status": "no_projects"}
        for pid in projects.get_all_project_ids():
            drift_state = intel.cognition.drift.get(pid)
            if drift_state.get("drift_strength", 0) > 0.8:
                intel.cognition.drift.state[pid]["drift_strength"] *= 0.5
        return {"status": "midnight_reset_complete"}

    async def run_daily_meta_learning(self):
        meta = self.registry.get_subsystem("meta")
        if meta:
            return meta.run_cycle()
        return {"status": "meta_unavailable"}

    async def run_periodic_orchestration_cycle(self):
        orchestrator = self.registry.get_subsystem("orchestrator")
        if orchestrator:
            return orchestrator.global_cycle()
        return {"status": "orchestrator_unavailable"}

    async def send_agent_keepalive(self) -> Dict[str, str]:
        intel = self.registry.get_subsystem("intelligence")
        projects = self._projects()
        if not intel or not projects:
            return {"status": "no_projects"}
        payload = {"heartbeat": datetime.utcnow().isoformat(), "message": "system_keepalive"}
        for pid in projects.get_all_project_ids():
            intel.cognition.push_memory(pid, payload)
        return {"status": "keepalive_sent"}
