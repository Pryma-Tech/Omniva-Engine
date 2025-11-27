"""
Uploader subsystem that handles OAuth + YouTube uploads.
"""

import os
from typing import Any, Dict, List

from app.core.event_bus import event_bus
from app.core.registry import registry

from .oauth_handler import OAuthHandler
from .youtube_uploader import YouTubeUploader


class UploaderSubsystem:
    """Upload rendered clips to YouTube via the Data API."""

    name = "uploader"

    def __init__(self) -> None:
        self.oauth = OAuthHandler()

    def initialize(self) -> Dict[str, str]:
        return {"status": "uploader subsystem initialized"}

    def upload_clips(self, clips: List[str], project_id: int) -> Dict[str, Any]:
        """Upload the provided clip filepaths."""
        if not clips:
            return {"error": "no clips provided", "project_id": project_id}

        creds = self.oauth.get_credentials()
        uploader = YouTubeUploader(creds)

        uploaded = []
        for clip in clips:
            if not os.path.exists(clip):
                uploaded.append({"clip": clip, "error": "file not found"})
                continue

            title = f"Clip {os.path.basename(clip)}"
            description = "Generated automatically by Omniva Engine"
            tags = ["shorts", "ai", "viral", "clip"]

            response = uploader.upload_video(clip, title, description, tags)
            uploaded.append({"clip": clip, "youtube_id": response.get("id")})

        result = {"project_id": project_id, "uploaded": uploaded}
        event_bus.publish("upload_complete", result)
        return result

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}


registry.register_subsystem("uploader", UploaderSubsystem())
