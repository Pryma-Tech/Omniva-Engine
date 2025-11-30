"""Filesystem-backed project store for the v0.1 backend."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Callable


def _noop_session_factory() -> None:  # pragma: no cover - placeholder for future DB
    return None


class ProjectStore:
    """Persist simple project metadata as JSON files.

    This is a direct adaptation of the omniva-v2 ProjectStore, with the
    storage base relocated under ``backend/storage/projects_meta`` and
    database hooks stubbed out for future use.
    """

    def __init__(
        self,
        base_path: str | None = None,
        session_factory: Callable[[], Any] | None = None,
    ) -> None:
        if base_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            default_base = os.path.join(base_dir, "..", "..", "storage", "projects_meta")
            self.base = os.path.abspath(default_base)
        else:
            self.base = os.path.abspath(base_path)
        os.makedirs(self.base, exist_ok=True)
        # TODO(omniva-v0.1): Replace JSON persistence with relational table once available.
        self._session_factory = session_factory or _noop_session_factory

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
            # TODO(omniva-v0.1): Implement relational project fetch using session once projects table exists.
            pass
        path = self._path(project_id)
        if not os.path.exists(path):
            return self._with_defaults(project_id, {})
        with open(path, "r", encoding="utf-8") as project_file:
            raw = json.load(project_file)
        return self._with_defaults(project_id, raw)

    def save(self, project_id: int, data: Dict[str, Any], session: Any | None = None) -> Dict[str, Any]:
        if session is not None:
            # TODO(omniva-v0.1): Persist project rows to the database once schema is defined.
            pass
        payload = self._with_defaults(project_id, data)
        path = self._path(project_id)
        with open(path, "w", encoding="utf-8") as project_file:
            json.dump(payload, project_file, indent=2)
        return payload

    def list_all(self, session: Any | None = None) -> List[Dict[str, Any]]:
        if session is not None:
            # TODO(omniva-v0.1): Query relational storage when available.
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
            # TODO(omniva-v0.1): Query relational storage when available.
            pass
        ids: List[int] = []
        for file_name in os.listdir(self.base):
            if not file_name.endswith(".json"):
                continue
            ids.append(int(file_name.replace(".json", "")))
        return sorted(ids)
