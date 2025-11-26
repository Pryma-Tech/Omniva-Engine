"""TranscriptJob model (placeholder)."""
# TODO: Add real ASR output, confidence scores, segments, diarization.

import time


class TranscriptJob:
    """Stores fake transcription data."""

    def __init__(self, job_id: int, project_id: int, video_path: str, text: str, segments: list):
        self.job_id = job_id
        self.project_id = project_id
        self.video_path = video_path
        self.text = text
        self.segments = segments
        self.timestamp = time.time()
        self.status = "completed (placeholder)"
