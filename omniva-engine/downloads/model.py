"""DownloadJob model (placeholder)."""
# TODO: Add real download metadata, timestamps, sizes, status flags.

import time


class DownloadJob:
    """Represents a fake download job."""

    def __init__(self, job_id: int, project_id: int, platform: str, source: str, fake_path: str):
        self.job_id = job_id
        self.project_id = project_id
        self.platform = platform
        self.source = source
        self.fake_path = fake_path
        self.timestamp = time.time()
        self.status = "completed (placeholder)"
