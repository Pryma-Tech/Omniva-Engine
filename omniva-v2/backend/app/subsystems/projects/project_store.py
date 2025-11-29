"""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/projects/project_store.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/projects/project_store with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/projects/project_store with cognitive telemetry.

Filesystem-backed project configuration store.
"""

import json
import os
from typing import Any, Dict, List


class ProjectStore:
    """Persist per-project metadata (creators, keywords, schedule)."""

    def __init__(self) -> None:
        self.base = os.path.join("storage", "projects_meta")
        os.makedirs(self.base, exist_ok=True)

    def _path(self, project_id: int) -> str:
        return os.path.join(self.base, f"{project_id}.json")

    def _with_defaults(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        defaults: Dict[str, Any] = {
            "project_id": project_id,
            "id": project_id,
            "creators": [],
            "keywords": [],
            "schedule": {"enabled": False, "cron": "0 */6 * * *"},
            "autonomous": False,
            "shadow_mode": True,
            "daily_limit": 3,
            "auto_publish_mode": "schedule",
            "clips": [],
        }
        merged = {**defaults, **(data or {})}
        merged["project_id"] = project_id
        merged["id"] = merged.get("id", project_id)
        return merged

    def get(self, project_id: int) -> Dict[str, Any]:
        path = self._path(project_id)
        if not os.path.exists(path):
            return self._with_defaults(project_id, {})
        with open(path, "r", encoding="utf-8") as project_file:
            raw = json.load(project_file)
        return self._with_defaults(project_id, raw)

    def save(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = self._with_defaults(project_id, data)
        path = self._path(project_id)
        with open(path, "w", encoding="utf-8") as project_file:
            json.dump(payload, project_file, indent=2)
        return payload

    def list_all(self) -> List[Dict[str, Any]]:
        projects: List[Dict[str, Any]] = []
        for file_name in os.listdir(self.base):
            if not file_name.endswith(".json"):
                continue
            project_id = int(file_name.replace(".json", ""))
            projects.append(self.get(project_id))
        return projects

    def list_ids(self) -> List[int]:
        ids: List[int] = []
        for file_name in os.listdir(self.base):
            if not file_name.endswith(".json"):
                continue
            ids.append(int(file_name.replace(".json", "")))
        return sorted(ids)
