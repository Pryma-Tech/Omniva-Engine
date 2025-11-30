"""Global scheduled tasks triggered by the Heartbeat engine."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict


class CronTasks:
    """Define global tasks executed on a schedule."""

    def __init__(self, registry, logger: logging.Logger | None = None) -> None:
        self.registry = registry
        self.logger = logger or logging.getLogger(__name__)

    def _projects(self):
        # TODO(omniva-v0.1): Cache project subsystem handles to reduce repeated lookups.
        return self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")

    def _log(self, action: str, **extra: Any) -> None:
        self.logger.info("cron_task.%s", action, extra=extra)

    async def run_daily_midnight_reset(self) -> Dict[str, str]:
        # TODO(omniva-v0.1): Replace placeholder drift logic with Horizon-aligned resets.
        # TODO(omniva-v0.2): Emit Stardust events describing reset actions.
        intel = self.registry.get_subsystem("intelligence")
        projects = self._projects()
        if not intel or not projects:
            payload = {"action": "midnight_reset", "status": "no_projects", "projects": 0}
            self._log("midnight_reset", **payload)
            return payload
        project_ids = projects.get_all_project_ids()
        for pid in project_ids:
            drift_state = intel.cognition.drift.get(pid)
            if drift_state.get("drift_strength", 0) > 0.8:
                intel.cognition.drift.state[pid]["drift_strength"] *= 0.5
        payload = {
            "action": "midnight_reset",
            "status": "midnight_reset_complete",
            "projects": len(project_ids),
        }
        self._log("midnight_reset", **payload)
        return payload

    async def run_daily_meta_learning(self):
        # TODO(omniva-v0.1): Define concrete meta-learning routines and metrics.
        meta = self.registry.get_subsystem("meta")
        if meta:
            result = meta.run_cycle()
            payload = {"action": "meta_learning", **result}
            self._log("meta_learning", **payload)
            return payload
        payload = {"action": "meta_learning", "status": "meta_unavailable"}
        self._log("meta_learning", **payload)
        return payload

    async def run_periodic_orchestration_cycle(self):
        # TODO(omniva-v0.1): Parameterize cadence per deployment configuration.
        orchestrator = self.registry.get_subsystem("orchestrator")
        if orchestrator:
            result = orchestrator.global_cycle()
            payload = {"action": "orchestration_cycle", "status": "ok", "result": result}
            self._log("orchestration_cycle", **payload)
            return payload
        payload = {"action": "orchestration_cycle", "status": "orchestrator_unavailable"}
        self._log("orchestration_cycle", **payload)
        return payload

    async def send_agent_keepalive(self) -> Dict[str, str]:
        # TODO(omniva-v0.1): Include subsystem health summaries in keepalive payload.
        # TODO(omniva-v0.2): Push keepalives to external monitoring bus.
        intel = self.registry.get_subsystem("intelligence")
        projects = self._projects()
        if not intel or not projects:
            payload = {"action": "agent_keepalive", "status": "no_projects", "projects": 0}
            self._log("agent_keepalive", **payload)
            return payload
        payload = {"heartbeat": datetime.utcnow().isoformat(), "message": "system_keepalive"}
        project_ids = projects.get_all_project_ids()
        for pid in project_ids:
            intel.cognition.push_memory(pid, payload)
        result = {
            "action": "agent_keepalive",
            "status": "keepalive_sent",
            "projects": len(project_ids),
        }
        self._log("agent_keepalive", **result)
        return result
