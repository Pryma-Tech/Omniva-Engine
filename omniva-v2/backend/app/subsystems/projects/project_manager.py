"""
Project manager subsystem.
"""

from typing import Any, Dict, List

from .project_store import ProjectStore


class ProjectManager:
    """Provide CRUD over project metadata."""

    name = "project_manager"

    def __init__(self) -> None:
        self.store = ProjectStore()

    def initialize(self) -> Dict[str, str]:
        return {"status": "project manager initialized"}

    def create(self, project_id: int) -> Dict[str, Any]:
        """Create a project record with defaults."""
        return self.store.save(project_id, {})

    def get(self, project_id: int) -> Dict[str, Any]:
        return self.store.get(project_id)

    def save(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.store.save(project_id, data)

    def list_projects(self) -> List[Dict[str, Any]]:
        return self.store.list_all()

    def list_all(self) -> List[Dict[str, Any]]:
        return self.store.list_all()

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}
