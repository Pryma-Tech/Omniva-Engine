"""Analysis models."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/models/analysis.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/models/analysis with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/models/analysis with cognitive telemetry.


from typing import List

from pydantic import BaseModel


class ClipCandidate(BaseModel):
    """Represents a scored clip selection."""

    start: float
    end: float
    text: str
    score: float
    keywords: List[str] = []
