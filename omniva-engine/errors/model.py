"""ErrorRecord data model (placeholder)."""
# TODO: Expand with stack traces, categories, severity, and DB storage.

import time


class ErrorRecord:
    """Simple error container."""

    def __init__(self, error_id: int, project_id: int, subsystem: str, message: str):
        self.error_id = error_id
        self.project_id = project_id
        self.subsystem = subsystem
        self.message = message
        self.timestamp = time.time()
        self.retry_count = 0
        self.resolved = False
