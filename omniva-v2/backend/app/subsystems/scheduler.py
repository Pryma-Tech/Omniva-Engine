"""Scheduler subsystem for Omniva Engine v2 (placeholder)."""

import time
from typing import Any, Dict, List

from app.core.registry import registry
from app.core.job_queue import job_queue
from app.models.scheduler import ScheduleRule


class SchedulerSubsystem:
    """Placeholder scheduling engine."""

    name = "scheduler"

    def __init__(self) -> None:
        self.rules: List[ScheduleRule] = []

    def initialize(self) -> dict:
        return {"status": "scheduler subsystem initialized (placeholder)"}

    def add_rule(self, rule: ScheduleRule) -> Dict[str, Any]:
        self.rules.append(rule)
        return {"added": rule.dict()}

    def list_rules(self) -> List[Dict[str, Any]]:
        return [rule.dict() for rule in self.rules]

    def evaluate_schedules(self) -> Dict[str, Any]:
        now = time.time()
        return {
            "timestamp": now,
            "evaluated_rules": [rule.dict() for rule in self.rules],
            "status": "placeholder evaluation only",
        }

    def trigger_pipeline(self, project_id: int) -> Dict[str, Any]:
        job_queue.enqueue("run_pipeline", {"project_id": project_id})
        return {"status": "pipeline enqueued", "project_id": project_id}

    def status(self) -> Dict[str, Any]:
        return {"name": self.name, "schedule_count": len(self.rules), "status": "ok (placeholder)"}


registry.register_subsystem("scheduler", SchedulerSubsystem())
