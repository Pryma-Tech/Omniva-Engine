"""
Asynchronous worker engine with configurable concurrency.
"""

import asyncio
from typing import Optional

from app.core.job_queue import job_queue


class WorkerEngine:
    """Background worker pool executing queued jobs."""

    def __init__(self, concurrency: int = 3) -> None:
        self.concurrency = concurrency
        self.running = False
        self._tasks: Optional[list[asyncio.Task]] = None

    async def worker_loop(self, worker_id: int) -> None:
        """Continuously process jobs while running flag is set."""
        while self.running:
            job = job_queue.dequeue()
            if not job:
                await asyncio.sleep(0.25)
                continue
            try:
                result = job.run()
                job_queue.finish_job(job.id, result)
            except Exception as exc:  # pylint: disable=broad-except
                job_queue.fail_job(job.id, str(exc))

    async def start(self) -> None:
        """Start the worker pool."""
        if self.running:
            return
        self.running = True
        self._tasks = [asyncio.create_task(self.worker_loop(i)) for i in range(self.concurrency)]
        await asyncio.gather(*self._tasks)

    def stop(self) -> None:
        """Signal all workers to stop."""
        self.running = False
        if self._tasks:
            for task in self._tasks:
                task.cancel()
        self._tasks = None
