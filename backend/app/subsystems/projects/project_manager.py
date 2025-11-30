"""Project manager subsystem for the v0.1 backend."""

from __future__ import annotations

from typing import Any, Dict, List

from .project_store import ProjectStore


class ProjectManager:
    """Provide CRUD over project metadata."""

    name = "project_manager"

    def __init__(self, store: ProjectStore | None = None) -> None:
        self.store = store or ProjectStore()
        self._ensure_default_project()

    def _ensure_default_project(self) -> None:
        """Seed a default project when no project files exist."""
        if self.store.list_ids():
            return
        self.create(1)

    def initialize(self) -> Dict[str, str]:
        return {"status": "project manager initialized"}

    def create(self, project_id: int) -> Dict[str, Any]:
        """Create a project record with defaults."""
        return self.store.save(project_id, {})

    def get(self, project_id: int) -> Dict[str, Any]:
        return self.store.get(project_id)

    def get_project_config(self, project_id: int) -> Dict[str, Any]:
        return self.store.get(project_id)

    def save(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.store.save(project_id, data)

    def list_projects(self) -> List[Dict[str, Any]]:
        return self.store.list_all()

    def list_all(self) -> List[Dict[str, Any]]:
        return self.store.list_all()

    def get_project_clips(self, project_id: int) -> List[Dict[str, Any]]:
        project = self.get(project_id)
        return list(project.get("clips", []))

    def get_all_project_ids(self) -> List[int]:
        return self.store.list_ids()

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}
