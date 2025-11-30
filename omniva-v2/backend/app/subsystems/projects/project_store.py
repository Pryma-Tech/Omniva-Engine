"""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/projects/project_store.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/projects/project_store with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/projects/project_store with cognitive telemetry.

Filesystem-backed project configuration store.
"""

import json
import os
from typing import Any, Callable, Dict, List, Optional

from app.models.db import SessionLocal


class ProjectStore:
    """Persist per-project metadata (creators, keywords, schedule)."""

    def __init__(self, session_factory: Optional[Callable[[], Any]] = None) -> None:
        self.base = os.path.join("storage", "projects_meta")
        os.makedirs(self.base, exist_ok=True)
        # TODO(omniva-v0.2): Replace JSON persistence with relational table once available.
        self._session_factory = session_factory or SessionLocal

    def _get_session(self):
        """Provide a database session for future relational storage."""
        return self._session_factory()

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

    def get(self, project_id: int, session: Any | None = None) -> Dict[str, Any]:
        if session is not None:
            # TODO(omniva-v0.2): Implement relational project fetch using session once projects table exists.
            pass
        path = self._path(project_id)
        if not os.path.exists(path):
            return self._with_defaults(project_id, {})
        with open(path, "r", encoding="utf-8") as project_file:
            raw = json.load(project_file)
        return self._with_defaults(project_id, raw)

    def save(self, project_id: int, data: Dict[str, Any], session: Any | None = None) -> Dict[str, Any]:
        if session is not None:
            # TODO(omniva-v0.2): Persist project rows to the database once schema is defined.
            pass
        payload = self._with_defaults(project_id, data)
        path = self._path(project_id)
        with open(path, "w", encoding="utf-8") as project_file:
            json.dump(payload, project_file, indent=2)
        return payload

    def list_all(self, session: Any | None = None) -> List[Dict[str, Any]]:
        if session is not None:
            # TODO(omniva-v0.2): Query relational storage when available.
            pass
        projects: List[Dict[str, Any]] = []
        for file_name in os.listdir(self.base):
            if not file_name.endswith(".json"):
                continue
            project_id = int(file_name.replace(".json", ""))
            projects.append(self.get(project_id))
        return projects

    def list_ids(self, session: Any | None = None) -> List[int]:
        if session is not None:
            # TODO(omniva-v0.2): Query relational storage when available.
            pass
        ids: List[int] = []
        for file_name in os.listdir(self.base):
            if not file_name.endswith(".json"):
                continue
            ids.append(int(file_name.replace(".json", "")))
        return sorted(ids)
