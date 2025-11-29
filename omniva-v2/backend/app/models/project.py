"""Project model (placeholder)."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/models/project.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/models/project with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/models/project with cognitive telemetry.

# TODO: Replace with Pydantic + database models.

from pydantic import BaseModel
from typing import List


class Project(BaseModel):
    project_id: int
    name: str
    keywords: List[str] = []
    recency_days: int = 7
    active: bool = False
