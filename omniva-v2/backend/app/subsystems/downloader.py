"""
Downloader subsystem wired to platform extractors.
"""

import os
from typing import Any, Dict

from app.core.event_bus import event_bus
from app.core.job_queue import job_queue
from app.core.registry import registry
from app.core.url_detector import URLDetector
from app.subsystems.downloaders.instagram_extractor import InstagramExtractor
from app.subsystems.downloaders.tiktok_extractor import TikTokExtractor
from app.subsystems.downloaders.youtube_extractor import YouTubeExtractor

EXTRACTORS = {
    "tiktok": TikTokExtractor(),
    "instagram": InstagramExtractor(),
    "youtube": YouTubeExtractor(),
}


class DownloadSubsystem:
    """Download media from supported platforms."""

    name = "download"

    def initialize(self) -> Dict[str, str]:
        return {"status": "download subsystem initialized"}

    def download_url(self, url: str, project_id: int) -> Dict[str, Any]:
        """Download the provided URL and emit completion events."""
        platform = URLDetector.detect(url)
        if platform == "unknown":
            return {"error": "unsupported platform", "url": url}

        extractor = EXTRACTORS[platform]
        output_dir = os.path.join("storage", "projects", str(project_id), "raw")
        os.makedirs(output_dir, exist_ok=True)

        try:
            filepath = extractor.download(url, output_dir)
            result = {"url": url, "platform": platform, "filepath": filepath}
            event_bus.publish("download_complete", result)
            job_queue.enqueue("transcribe", {"filepath": filepath, "project_id": project_id})
            return result
        except Exception as exc:  # pylint: disable=broad-except
            return {"error": str(exc), "url": url, "platform": platform}

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}


registry.register_subsystem("download", DownloadSubsystem())
