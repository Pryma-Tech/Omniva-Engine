"""Pipeline model (placeholder)."""

from typing import Dict, List

from pydantic import BaseModel


class PipelineStep(BaseModel):
    name: str
    status: str
    metadata: Dict[str, str] | None = None


class PipelineRun(BaseModel):
    project_id: int
    steps: List[PipelineStep]
    status: str = "pending"
