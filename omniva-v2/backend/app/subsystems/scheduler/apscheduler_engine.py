"""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/scheduler/apscheduler_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/scheduler/apscheduler_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/scheduler/apscheduler_engine with cognitive telemetry.

AsyncIO-backed scheduler wrapper.
"""

from typing import Awaitable, Callable, Dict

from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


class APSchedulerEngine:
    """Manage cron jobs via APScheduler."""

    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        self.jobs: Dict[int, str] = {}

    def schedule_project(self, project_id: int, cron: str, callback: Callable[[], Awaitable[None]]) -> None:
        """Register or replace a cron job for the given project."""
        self.cancel_project(project_id)
        trigger = CronTrigger.from_crontab(cron)
        job = self.scheduler.add_job(callback, trigger, id=f"project_{project_id}")
        self.jobs[project_id] = job.id

    def cancel_project(self, project_id: int) -> None:
        """Remove an existing scheduled job."""
        job_id = self.jobs.pop(project_id, None)
        if not job_id:
            return
        try:
            self.scheduler.remove_job(job_id)
        except JobLookupError:
            pass
