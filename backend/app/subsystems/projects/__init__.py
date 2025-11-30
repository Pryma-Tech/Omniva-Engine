"""Project subsystem for the v0.1 backend.

This package provides a lightweight JSON-backed `ProjectStore` and a
thin `ProjectManager` facade, adapted from the omniva-v2 backend.
"""

from .project_manager import ProjectManager
from .project_store import ProjectStore

__all__ = ["ProjectManager", "ProjectStore"]

