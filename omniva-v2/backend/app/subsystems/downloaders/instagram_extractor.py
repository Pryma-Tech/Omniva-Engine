"""Instagram downloader powered by yt-dlp."""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/downloaders/instagram_extractor with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/downloaders/instagram_extractor with cognitive telemetry.

import os

import yt_dlp

from .base_extractor import BaseExtractor


class InstagramExtractor(BaseExtractor):
    """Download Instagram posts/reels with yt-dlp."""

    def download(self, url: str, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        ydl_opts = {
            "outtmpl": os.path.join(output_dir, "%(id)s.%(ext)s"),
            "quiet": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info)
