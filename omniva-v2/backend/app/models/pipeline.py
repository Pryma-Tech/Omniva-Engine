"""Pipeline model (placeholder)."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/models/pipeline.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/models/pipeline with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/models/pipeline with cognitive telemetry.


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
