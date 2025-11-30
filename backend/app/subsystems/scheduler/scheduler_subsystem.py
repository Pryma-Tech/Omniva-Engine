"""Small scheduler facade compatible with intelligence routes."""

from __future__ import annotations

from typing import Any, Dict

from .schedule_store import ScheduleStore


class SchedulerSubsystem:
    """Expose per-project schedule configuration."""

    def __init__(self, store: ScheduleStore | None = None) -> None:
        self.store = store or ScheduleStore()

    def get_project_schedule(self, project_id: int) -> Dict[str, Any]:
        return self.store.load(project_id)

    def configure_project(self, project_id: int, enabled: bool, cron: str) -> Dict[str, Any]:
        return self.store.save(project_id, {"enabled": bool(enabled), "cron": str(cron)})

