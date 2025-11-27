"""
Cron-based scheduling subsystem backed by APScheduler.
"""

from typing import Any, Dict

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

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}


registry.register_subsystem("scheduler", SchedulingSubsystem())
