"""LogManager handles in-memory log storage."""
# TODO: Implement file-backed log rotation or DB persistence.

from utils.logger import logger

from .model import LogRecord


class LogManager:
    """Provide a simple log recording interface."""

    def __init__(self):
        self.logs = {}
        self.next_id = 1
        logger.info("LogManager initialized (placeholder).")

    def log(self, subsystem: str, message: str) -> LogRecord:
        record = LogRecord(self.next_id, subsystem, message)
        self.logs[self.next_id] = record
        self.next_id += 1
        return record

    def list_all(self) -> list:
        return list(self.logs.values())

    def list_by_subsystem(self, subsystem: str) -> list:
        return [rec for rec in self.logs.values() if rec.subsystem == subsystem]
