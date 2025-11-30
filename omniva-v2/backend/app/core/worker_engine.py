"""Worker engine with concurrency, retries, and watchdog monitoring."""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/core/worker_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/core/worker_engine with cognitive telemetry.

import asyncio
from datetime import datetime
from typing import List

from app.core.event_bus import event_bus
from app.core.job_queue import job_queue


class WorkerEngine:
    """Asynchronous worker pool with retry/backoff logic."""

    def __init__(self, concurrency: int = 3) -> None:
        self.concurrency = concurrency
        self.running = False
        self._tasks: List[asyncio.Task] = []

    async def worker_loop(self, worker_id: int) -> None:
        while self.running:
            job = job_queue.dequeue()
            if not job:
                await asyncio.sleep(0.25)
                continue
            try:
                result = job.run()
                job_queue.finish_job(job.id, result)
            except Exception as exc:  # pylint: disable=broad-except
                attempts = job["attempts"]
                if attempts < 5:
                    backoff = 2 ** attempts
                    job_queue.retry_job(job.id, backoff)
                    event_bus.publish(
                        "job_retry_scheduled",
                        {"job_id": job.id, "attempts": attempts + 1, "backoff_seconds": backoff},
                    )
                else:
                    job_queue.fail_job(job.id, str(exc))
                    event_bus.publish("job_failed", {"job_id": job.id, "error": str(exc)})

    async def retry_loop(self) -> None:
        while self.running:
            now = datetime.utcnow()
            for job_id, job in list(job_queue.jobs.items()):
                if job.get("status") == "retrying":
                    retry_time = datetime.fromisoformat(job["retry_after"])
                    if retry_time <= now:
                        job_queue.requeue(job_id)
                        event_bus.publish("job_requeued", {"job_id": job_id})
            await asyncio.sleep(1)

    async def watchdog_loop(self) -> None:
        while self.running:
            now = datetime.utcnow()
            for job_id, job in list(job_queue.jobs.items()):
                if job.get("status") == "running":
                    started = datetime.fromisoformat(job["started"])
                    if (now - started).total_seconds() > 300:
                        job_queue.retry_job(job_id, 5)
                        event_bus.publish("job_timeout", {"job_id": job_id})
            await asyncio.sleep(10)

    async def start(self) -> None:
        if self.running:
            return
        self.running = True
        worker_tasks = [asyncio.create_task(self.worker_loop(i)) for i in range(self.concurrency)]
        worker_tasks.append(asyncio.create_task(self.retry_loop()))
        worker_tasks.append(asyncio.create_task(self.watchdog_loop()))
        self._tasks = worker_tasks
        await asyncio.gather(*worker_tasks)

    def stop(self) -> None:
        self.running = False
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()
