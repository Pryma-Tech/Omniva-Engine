"""
Cron-based scheduling subsystem backed by APScheduler.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List

from app.core.registry import registry

from .apscheduler_engine import APSchedulerEngine
from .schedule_store import ScheduleStore


class SchedulingSubsystem:
    """Manage per-project cron schedules for pipeline automation."""

    name = "scheduler"

    def __init__(self) -> None:
        self.store = ScheduleStore()
        self.engine = APSchedulerEngine()

    def initialize(self) -> Dict[str, str]:
        return {"status": "scheduler subsystem initialized"}

    async def _pipeline_trigger(self, project_id: int) -> None:
        manager = registry.get_subsystem("project_manager")
        orchestrator = registry.get_subsystem("orchestrator")
        config = manager.get(project_id)
        creators = config.get("creators", [])
        orchestrator.run_pipeline(project_id, creators)

    def configure_project(self, project_id: int, enabled: bool, cron: str) -> Dict[str, Any]:
        data = {"enabled": enabled, "cron": cron}
        self.store.save_project_schedule(project_id, data)

        if enabled:
            async def callback() -> None:
                await self._pipeline_trigger(project_id)

            self.engine.schedule_project(project_id, cron, callback)
        else:
            self.engine.cancel_project(project_id)
        return data

    def get_project_schedule(self, project_id: int) -> Dict[str, Any]:
        return self.store.get_project_schedule(project_id)

    def queue_clip(self, project_id: int, filepath: str, reason: str = "") -> Dict[str, Any]:
        """
        Persist a scheduled clip request for later publishing.
        """
        queue_dir = os.path.join("storage", "projects", str(project_id), "queue")
        os.makedirs(queue_dir, exist_ok=True)
        queue_path = os.path.join(queue_dir, "clips.json")
        record = {
            "project_id": project_id,
            "file": filepath,
            "reason": reason,
            "queued_at": datetime.utcnow().isoformat(),
        }
        existing: List[Dict[str, Any]] = []
        if os.path.exists(queue_path):
            with open(queue_path, "r", encoding="utf-8") as queue_file:
                existing = json.load(queue_file)
        existing.append(record)
        with open(queue_path, "w", encoding="utf-8") as queue_file:
            json.dump(existing, queue_file, indent=2)
        return record

    def suggest_post_time(self, project_id: int) -> Dict[str, Any]:
        """
        Surface either a predictive suggestion or the configured schedule.
        """
        intel = registry.get_subsystem("intelligence")
        suggestion: Dict[str, Any] = {}
        if intel and hasattr(intel, "choose_posting_time"):
            try:
                suggestion = intel.choose_posting_time(project_id)
            except Exception:  # pragma: no cover - prediction fallback
                suggestion = {}
        schedule = self.store.get_project_schedule(project_id)
        return {
            "project_id": project_id,
            "suggestion": suggestion,
            "schedule": schedule,
        }

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}


registry.register_subsystem("scheduler", SchedulingSubsystem())
