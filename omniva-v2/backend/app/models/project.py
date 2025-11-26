"""Project model (placeholder)."""
# TODO: Replace with Pydantic + database models.

from pydantic import BaseModel
from typing import List


class Project(BaseModel):
    project_id: int
    name: str
    keywords: List[str] = []
    recency_days: int = 7
    active: bool = False
