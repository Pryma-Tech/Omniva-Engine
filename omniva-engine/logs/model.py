"""LogRecord model (placeholder)."""
# TODO: Expand severity, type, project mapping, timestamps, formatting.

import time


class LogRecord:
    """Represents a single log entry."""

    def __init__(self, log_id: int, subsystem: str, message: str):
        self.log_id = log_id
        self.subsystem = subsystem
        self.message = message
        self.timestamp = time.time()
