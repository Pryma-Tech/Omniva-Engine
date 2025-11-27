"""
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

    def get(self, project_id: int) -> Dict[str, Any]:
        path = self._path(project_id)
        if not os.path.exists(path):
            return {
                "project_id": project_id,
                "creators": [],
                "keywords": [],
                "schedule": {"enabled": False, "cron": "0 */6 * * *"},
            }
        with open(path, "r", encoding="utf-8") as project_file:
            return json.load(project_file)

    def save(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        data["project_id"] = project_id
        path = self._path(project_id)
        with open(path, "w", encoding="utf-8") as project_file:
            json.dump(data, project_file, indent=2)
        return data

    def list_all(self) -> List[Dict[str, Any]]:
        projects: List[Dict[str, Any]] = []
        for file_name in os.listdir(self.base):
            if not file_name.endswith(".json"):
                continue
            project_id = int(file_name.replace(".json", ""))
            projects.append(self.get(project_id))
        return projects
