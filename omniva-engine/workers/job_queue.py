"""Simple job queue skeleton."""
# TODO: Replace with Redis/RQ, Celery, or async queue.

from utils.logger import logger


class JobQueue:
    """Placeholder FIFO queue for worker jobs."""

    def __init__(self):
        self.queue = []
        logger.info("JobQueue initialized (placeholder).")

    def enqueue(self, task: dict) -> dict:
        """Add job to queue."""
        logger.info("Enqueuing job (placeholder): %s", task)
        self.queue.append(task)
        return task

    def dequeue(self):
        """Remove next job from queue."""
        if not self.queue:
            logger.info("JobQueue empty (placeholder).")
            return None
        task = self.queue.pop(0)
        logger.info("Dequeued job (placeholder): %s", task)
        return task

    def size(self) -> int:
        """Return number of pending jobs."""
        return len(self.queue)
