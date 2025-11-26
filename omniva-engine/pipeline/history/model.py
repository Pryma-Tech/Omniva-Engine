"""PipelineRun data model (placeholder)."""
# TODO: Replace with real DB model and proper timestamps.

import time


class PipelineRun:
    """Simple data container for pipeline runs."""

    def __init__(self, run_id: int, project_id: int, steps: list, status: str):
        self.run_id = run_id
        self.project_id = project_id
        self.steps = steps
        self.status = status
        self.timestamp = time.time()
