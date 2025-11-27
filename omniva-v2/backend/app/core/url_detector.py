"""
Utility helpers for determining which platform a URL belongs to.
"""

import re
from typing import Literal


class URLDetector:
    """Simple pattern-based platform detection."""

    TIKTOK = re.compile(r"tiktok\.com", re.IGNORECASE)
    INSTAGRAM = re.compile(r"instagram\.com|instagr\.am", re.IGNORECASE)
    YOUTUBE = re.compile(r"youtube\.com|youtu\.be", re.IGNORECASE)

    @staticmethod
    def detect(url: str) -> Literal["tiktok", "instagram", "youtube", "unknown"]:
        """
        Inspect the URL and return which downstream extractor should handle it.
        """
        if URLDetector.TIKTOK.search(url):
            return "tiktok"
        if URLDetector.INSTAGRAM.search(url):
            return "instagram"
        if URLDetector.YOUTUBE.search(url):
            return "youtube"
        return "unknown"
