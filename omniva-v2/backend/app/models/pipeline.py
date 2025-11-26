"""Pipeline model (placeholder)."""

from pydantic import BaseModel
from typing import List, Dict


class ClipCandidate(BaseModel):
    start: float
    end: float
    text: str
    score: float


class PipelineStep(BaseModel):
    name: str
    status: str
    metadata: Dict[str, str] | None = None


class PipelineRun(BaseModel):
    project_id: int
    steps: List[PipelineStep]
    status: str = "pending"
