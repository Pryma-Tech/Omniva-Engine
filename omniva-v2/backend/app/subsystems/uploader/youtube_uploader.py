"""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/uploader/youtube_uploader.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/uploader/youtube_uploader with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/uploader/youtube_uploader with cognitive telemetry.

Thin wrapper for uploading clips to YouTube.
"""

from typing import List

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class YouTubeUploader:
    """Handles YouTube Data API interactions."""

    def __init__(self, credentials) -> None:
        self.service = build("youtube", "v3", credentials=credentials)

    def upload_video(self, filepath: str, title: str, description: str, tags: List[str]) -> dict:
        """Upload a single video file."""
        request = self.service.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": "22",
                },
                "status": {
                    "privacyStatus": "public",
                },
            },
            media_body=MediaFileUpload(filepath, chunksize=-1, resumable=True),
        )

        response = None
        while response is None:
            _, response = request.next_chunk()
        return response
