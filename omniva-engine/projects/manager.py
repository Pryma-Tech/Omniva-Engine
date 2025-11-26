"""ProjectManager handles in-memory project CRUD."""
# TODO: Replace with database backend.

from utils.logger import logger

from .model import Project


class ProjectManager:
    """In-memory storage for projects."""

    def __init__(self):
        self.projects = {}
        self.next_id = 1
        logger.info("ProjectManager initialized (placeholder).")

    def create(self, name: str, keywords: list, recency_days: int = 7) -> Project:
        pid = self.next_id
        self.next_id += 1
        project = Project(pid, name, keywords, recency_days)
        self.projects[pid] = project
        try:
            from api.main import log_manager
            log_manager.log("projects", f"Created project {pid} (placeholder)")
        except Exception:  # pragma: no cover
            pass
        return project

    def get(self, project_id: int):
        return self.projects.get(project_id)

    def list(self):
        return list(self.projects.values())

    def update_keywords(self, project_id: int, keywords: list):
        project = self.get(project_id)
        if project:
            project.keywords = keywords
            try:
                from api.main import log_manager
                log_manager.log("projects", f"Updated keywords for project {project_id} (placeholder)")
            except Exception:  # pragma: no cover
                pass
        return project

    def add_creator(self, project_id: int, creator: dict):
        project = self.get(project_id)
        if project:
            project.creators.append(creator)
            try:
                from api.main import log_manager
                log_manager.log("projects", f"Added creator to project {project_id} (placeholder)")
            except Exception:  # pragma: no cover
                pass
        return project

    def toggle_active(self, project_id: int):
        project = self.get(project_id)
        if project:
            project.active = not project.active
            try:
                from api.main import log_manager
                log_manager.log("projects", f"Toggled project {project_id} active state (placeholder)")
            except Exception:  # pragma: no cover
                pass
        return project
