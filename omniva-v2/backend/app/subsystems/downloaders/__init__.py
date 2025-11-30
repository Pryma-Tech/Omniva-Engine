"""Extractor plugin package."""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/downloaders/__init__ with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/downloaders/__init__ with cognitive telemetry.


from .tiktok_extractor import TikTokExtractor
from .instagram_extractor import InstagramExtractor
from .youtube_extractor import YouTubeExtractor
from .base_extractor import BaseExtractor

__all__ = [
    "BaseExtractor",
    "TikTokExtractor",
    "InstagramExtractor",
    "YouTubeExtractor",
]
