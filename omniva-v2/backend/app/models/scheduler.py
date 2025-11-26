"""Scheduler models (placeholder)."""

from pydantic import BaseModel


class ScheduleRule(BaseModel):
    project_id: int
    cron: str
    description: str = "placeholder rule"
