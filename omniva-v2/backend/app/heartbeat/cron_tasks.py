"""Global scheduled tasks triggered by the Heartbeat engine (v2)."""

from __future__ import annotations

import logging
from datetime import datetime
from statistics import mean
from typing import Any, Dict, List


class CronTasks:
    """Define global tasks executed on a schedule."""

    def __init__(self, registry, logger: logging.Logger | None = None) -> None:
        self.registry = registry
        self.logger = logger or logging.getLogger(__name__)
        self._project_cache = None
        self._horizon_cache = None

    def _projects(self):
        if self._project_cache is not None:
            return self._project_cache
        subsystem = self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")
        if subsystem is not None:
            self._project_cache = subsystem
        return subsystem

    def _horizon(self):
        if self._horizon_cache is not None:
            return self._horizon_cache
        horizon = self.registry.get_subsystem("horizon")
        if horizon is not None:
            self._horizon_cache = horizon
        return horizon

    def _log(self, action: str, **extra: Any) -> None:
        self.logger.info("cron_task.%s", action, extra=extra)

    async def run_daily_midnight_reset(self) -> Dict[str, str]:
        intel = self.registry.get_subsystem("intelligence")
        projects = self._projects()
        horizon = self._horizon()
        if not intel or not projects:
            payload = {"action": "midnight_reset", "status": "no_projects", "projects": 0, "adjustments": []}
            self._log("midnight_reset", **payload)
            return payload
        project_ids = projects.get_all_project_ids()
        adjustments: List[Dict[str, Any]] = []
        for pid in project_ids:
            drift_state = intel.cognition.drift.get(pid)
            goal = horizon.get_epoch_goal(pid)["goals"] if horizon else {}
            target = float(goal.get("drift_target", 0.5 if goal else 0.4))
            current = drift_state.get("drift_strength", 0.0)
            if current > target:
                updated = max(target, current * 0.55)
            elif current > 0:
                updated = max(0.05, min(target, current))
            else:
                updated = target
            intel.cognition.drift.state[pid]["drift_strength"] = round(updated, 4)
            adjustments.append(
                {
                    "project_id": pid,
                    "before": round(current, 4),
                    "after": round(updated, 4),
                    "target": target,
                    "horizon_goal": bool(goal),
                }
            )
        payload = {
            "action": "midnight_reset",
            "status": "midnight_reset_complete",
            "projects": len(project_ids),
            "adjustments": adjustments,
        }
        self._log("midnight_reset", **payload)
        return payload

    async def run_daily_meta_learning(self):
        meta = self.registry.get_subsystem("meta")
        intel = self.registry.get_subsystem("intelligence")
        projects = self._projects()
        if meta and intel and projects:
            result = meta.run_cycle()
            project_ids = projects.get_all_project_ids()
            drift_values = [intel.cognition.drift.get(pid).get("drift_strength", 0.0) for pid in project_ids]
            avg_drift = mean(drift_values) if drift_values else 0.0
            payload = {
                "action": "meta_learning",
                "status": "ok",
                "iteration": result.get("iteration"),
                "projects_reviewed": len(project_ids),
                "avg_drift": avg_drift,
                "max_drift": max(drift_values) if drift_values else 0.0,
            }
            self._log("meta_learning", **payload)
            return payload
        payload = {"action": "meta_learning", "status": "meta_unavailable"}
        self._log("meta_learning", **payload)
        return payload

    async def run_periodic_orchestration_cycle(self):
        cadence = 0.0
        if getattr(self.registry, "config", None):
            cadence = getattr(self.registry.config.heartbeat, "orchestrator_interval", 0.0)
        orchestrator = self.registry.get_subsystem("orchestrator")
        if orchestrator:
            result = orchestrator.global_cycle()
            payload = {
                "action": "orchestration_cycle",
                "status": "ok",
                "result": result,
                "cadence_seconds": cadence,
            }
            self._log("orchestration_cycle", **payload)
            return payload
        payload = {"action": "orchestration_cycle", "status": "orchestrator_unavailable"}
        self._log("orchestration_cycle", **payload)
        return payload

    async def send_agent_keepalive(self) -> Dict[str, str]:
        intel = self.registry.get_subsystem("intelligence")
        projects = self._projects()
        health = getattr(self.registry, "health", None)
        if not intel or not projects:
            payload = {
                "action": "agent_keepalive",
                "status": "no_projects",
                "projects": 0,
                "health": {},
            }
            self._log("agent_keepalive", **payload)
            return payload
        payload = {"heartbeat": datetime.utcnow().isoformat(), "message": "system_keepalive"}
        project_ids = projects.get_all_project_ids()
        for pid in project_ids:
            intel.cognition.push_memory(pid, payload)
        result: Dict[str, Any] = {
            "action": "agent_keepalive",
            "status": "keepalive_sent",
            "projects": len(project_ids),
            "health": health.system_health() if health else {},
        }
        self._log("agent_keepalive", **result)
        return result

