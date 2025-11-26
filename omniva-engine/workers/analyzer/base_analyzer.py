"""Base analyzer class for Omniva Engine."""
# TODO: Implement real AI and heuristic analysis.

from abc import ABC, abstractmethod
from typing import List


class BaseAnalyzer(ABC):
    """Abstract analyzer contract for future AI pipelines."""

    def __init__(self, project_id: int, video_path: str, keywords: List[str]):
        self.project_id = project_id
        self.video_path = video_path
        self.keywords = keywords

    @abstractmethod
    def run_analysis(self):
        """Return structured clip candidate data."""
