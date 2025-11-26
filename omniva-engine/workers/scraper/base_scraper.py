"""Base scraper class for all platforms."""
# TODO: Implement platform-specific scraping logic in subclasses.

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from utils.logger import logger


class BaseScraper(ABC):
    """Abstract base class for all scrapers."""

    def __init__(self, project_id: int, creator_data: Dict[str, Any]) -> None:
        self.project_id = project_id
        self.creator_data = creator_data
        logger.info(
            "Initialized %s for project %s (placeholder).",
            self.__class__.__name__,
            project_id,
        )

    @abstractmethod
    def fetch_recent_posts(self, recency_days: int) -> List[Dict[str, Any]]:
        """Fetch posts for the creator within the recency window."""

    @abstractmethod
    def download_video(self, post_data: Dict[str, Any]) -> Any:
        """Download the video for a given post."""
