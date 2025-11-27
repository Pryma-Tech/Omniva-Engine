"""Analysis models."""

from typing import List

from pydantic import BaseModel


class ClipCandidate(BaseModel):
    """Represents a scored clip selection."""

    start: float
    end: float
    text: str
    score: float
    keywords: List[str] = []
