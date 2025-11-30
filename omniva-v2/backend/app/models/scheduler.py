"""Scheduler models."""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/models/scheduler with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/models/scheduler with cognitive telemetry.


from pydantic import BaseModel


class ScheduleRule(BaseModel):
    project_id: int
    cron: str
    description: str = "placeholder rule"
