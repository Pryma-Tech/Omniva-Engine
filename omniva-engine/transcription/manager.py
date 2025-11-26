"""TranscriptionManager placeholder."""
# TODO: Integrate real transcription backend.

from utils.logger import logger

from .model import TranscriptJob


class TranscriptionManager:
    """Generate fake transcripts for testing."""

    def __init__(self):
        self.jobs = {}
        self.next_id = 1
        logger.info("TranscriptionManager initialized (placeholder).")

    def transcribe(self, project_id: int, video_path: str) -> TranscriptJob:
        job_id = self.next_id
        self.next_id += 1
        fake_text = "This is a placeholder transcript. Real transcription will be implemented later."
        fake_segments = [
            {"start": 0.0, "end": 2.5, "text": "Hello"},
            {"start": 2.5, "end": 5.0, "text": "This is placeholder speech"},
        ]
        job = TranscriptJob(job_id, project_id, video_path, fake_text, fake_segments)
        self.jobs[job_id] = job
        return job

    def list_all(self) -> list:
        return list(self.jobs.values())

    def list_by_project(self, project_id: int) -> list:
        return [job for job in self.jobs.values() if job.project_id == project_id]
