"\"\"\"TikTok discovery via yt-dlp.\"\"\""

import yt_dlp


def discover_tiktok_posts(profile_url: str) -> list[str]:
    """Return recent TikTok post URLs for the profile."""
    options = {"quiet": True, "extract_flat": True}
    urls: list[str] = []
    with yt_dlp.YoutubeDL(options) as ydl:
        data = ydl.extract_info(profile_url, download=False)
        for entry in data.get("entries", []):
            url = entry.get("url")
            if url:
                urls.append(url)
    return urls
