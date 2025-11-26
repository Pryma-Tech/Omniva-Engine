"""DownloadManager (Placeholder)."""
# TODO: Integrate actual download routines.

from utils.logger import logger

from .model import DownloadJob


class DownloadManager:
    """Manage fake download jobs."""

    def __init__(self):
        logger.info("DownloadManager initialized (placeholder).")
        self.jobs = {}
        self.next_id = 1

    def download(self, project_id: int, platform: str, source: str) -> DownloadJob:
        job_id = self.next_id
        self.next_id += 1
        fake_path = f"storage_root/project_{project_id}/downloads/fake_video_{job_id}.mp4"
        job = DownloadJob(job_id, project_id, platform, source, fake_path)
        self.jobs[job_id] = job
        logger.info("Fake download recorded: job %s", job_id)
        return job

    def list_all(self) -> list:
        return list(self.jobs.values())

    def list_by_project(self, project_id: int) -> list:
        return [job for job in self.jobs.values() if job.project_id == project_id]
