"""Lightweight Project model for configuration APIs.

This v0.1 model is intentionally minimal and in-memory only; it is used
to validate and document payloads flowing through the projects API and
`ProjectManager`. A future revision can swap this for richer Pydantic
and database-backed models.
"""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/models/project with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/models/project with cognitive telemetry.

from typing import List, Optional

from pydantic import BaseModel


class Project(BaseModel):
    project_id: int
    name: str
    keywords: List[str] = []
    recency_days: int = 7
    active: bool = False
    autonomous: Optional[bool] = None
