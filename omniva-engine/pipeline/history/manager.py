"""In-memory Pipeline History Manager."""
# TODO: Persist run history in a database.

from utils.logger import logger

from .model import PipelineRun


class PipelineHistoryManager:
    """Store pipeline runs for reference."""

    def __init__(self):
        self.runs = {}
        self.next_id = 1
        logger.info("PipelineHistoryManager initialized (placeholder).")

    def record(self, project_id: int, steps: list, status: str) -> PipelineRun:
        run = PipelineRun(self.next_id, project_id, steps, status)
        self.runs[self.next_id] = run
        self.next_id += 1
        return run

    def list(self) -> list:
        return list(self.runs.values())

    def list_by_project(self, project_id: int) -> list:
        return [run for run in self.runs.values() if run.project_id == project_id]
