"""Project manager subsystem.

Provides a thin abstraction over :class:`ProjectStore` so that the rest
of the system can treat project configuration as a subsystem. This v0.1
implementation is intentionally simple and delegates persistence details
to the underlying store.
"""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/projects/project_manager with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/projects/project_manager with cognitive telemetry.

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
