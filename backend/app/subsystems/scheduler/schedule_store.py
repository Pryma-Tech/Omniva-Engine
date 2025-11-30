"""Filesystem-backed schedule store used by the scheduler subsystem."""

from __future__ import annotations

import json
import os
from typing import Any, Dict


class ScheduleStore:
    """Persist simple cron configuration per project."""

    def __init__(self, base_dir: str | None = None) -> None:
        if base_dir is None:
            base_dir = os.path.join("backend", "storage", "scheduler")
        self.base = os.path.abspath(base_dir)
        os.makedirs(self.base, exist_ok=True)

    def _path(self, project_id: int) -> str:
        return os.path.join(self.base, f"{project_id}.json")

    def load(self, project_id: int) -> Dict[str, Any]:
        path = self._path(project_id)
        if not os.path.exists(path):
            return {"project_id": project_id, "enabled": False, "cron": "0 */6 * * *"}
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        data.setdefault("project_id", project_id)
        data.setdefault("enabled", False)
        data.setdefault("cron", "0 */6 * * *")
        return data

    def save(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = self.load(project_id)
        payload.update(data or {})
        payload["project_id"] = project_id
        with open(self._path(project_id), "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        return payload

