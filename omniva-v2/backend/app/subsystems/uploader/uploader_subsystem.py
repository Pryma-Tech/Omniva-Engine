"""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/uploader/uploader_subsystem.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/uploader/uploader_subsystem with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/uploader/uploader_subsystem with cognitive telemetry.

Uploader subsystem that handles OAuth + YouTube uploads.
"""

import asyncio
import os
from datetime import datetime
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

    async def upload(self, project_id: int, clip: str) -> Dict[str, Any]:
        """
        Async wrapper for the autonomous loop.
        """
        return await asyncio.to_thread(self.upload_clips, [clip], project_id)

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
            try:
                intelligence = registry.get_subsystem("intelligence")
                intelligence.posting_time.record_post(project_id, datetime.utcnow())
            except Exception:  # pylint: disable=broad-except
                pass

        result = {"project_id": project_id, "uploaded": uploaded}
        event_bus.publish("upload_complete", result)
        return result

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}


registry.register_subsystem("uploader", UploaderSubsystem())
