# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/discovery/scrapers/youtube.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/discovery/scrapers/youtube with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/discovery/scrapers/youtube with cognitive telemetry.

"\"\"\"YouTube discovery via yt-dlp.\"\"\""

from typing import List

import yt_dlp


def discover_youtube_posts(channel_url: str) -> List[str]:
    """Return watch URLs for channel uploads."""
    options = {"quiet": True, "extract_flat": True}
    urls: List[str] = []
    with yt_dlp.YoutubeDL(options) as ydl:
        data = ydl.extract_info(channel_url, download=False)
        for entry in data.get("entries", []):
            entry_id = entry.get("id")
            if entry_id:
                urls.append(f"https://www.youtube.com/watch?v={entry_id}")
    return urls
