"""ErrorManager stores pipeline and system errors (placeholder)."""
# TODO: Implement persistence, automatic retries, severity levels.

from utils.logger import logger

from .model import ErrorRecord


class ErrorManager:
    """In-memory error tracking."""

    def __init__(self):
        self.errors = {}
        self.next_id = 1
        logger.info("ErrorManager initialized (placeholder).")

    def record(self, project_id: int, subsystem: str, message: str) -> ErrorRecord:
        error = ErrorRecord(self.next_id, project_id, subsystem, message)
        self.errors[self.next_id] = error
        self.next_id += 1
        return error

    def list_all(self) -> list:
        return list(self.errors.values())

    def list_by_project(self, project_id: int) -> list:
        return [err for err in self.errors.values() if err.project_id == project_id]

    def retry(self, error_id: int):
        err = self.errors.get(error_id)
        if err:
            err.retry_count += 1
        return err

    def resolve(self, error_id: int):
        err = self.errors.get(error_id)
        if err:
            err.resolved = True
        return err
