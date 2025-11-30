"""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/scheduler/schedule_store.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/scheduler/schedule_store with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/scheduler/schedule_store with cognitive telemetry.

Persistent schedule storage per project.
"""

import json
import os
from typing import Any, Dict


class ScheduleStore:
    """Simple JSON-backed schedule store."""

    def __init__(self) -> None:
        self.base = os.path.join("storage", "schedules")
        os.makedirs(self.base, exist_ok=True)

    def get_project_schedule(self, project_id: int) -> Dict[str, Any]:
        path = os.path.join(self.base, f"{project_id}.json")
        if not os.path.exists(path):
            return {"enabled": False, "cron": "0 */6 * * *"}
        with open(path, "r", encoding="utf-8") as project_file:
            return json.load(project_file)

    def save_project_schedule(self, project_id: int, data: Dict[str, Any]) -> None:
        path = os.path.join(self.base, f"{project_id}.json")
        with open(path, "w", encoding="utf-8") as project_file:
            json.dump(data, project_file, indent=2)
