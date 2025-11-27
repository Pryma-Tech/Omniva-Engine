"""
Abstract base class for download extractors.
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseExtractor(ABC):
    """Shared interface for all downloader plugins."""

    @abstractmethod
    def download(self, url: str, output_dir: str) -> Optional[str]:
        """
        Download the provided URL into the output directory.
        Returns the downloaded filename on success and None on failure.
        """

