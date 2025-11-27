"""
Autonomous mode engine for Omniva Engine v2.
"""

import asyncio
import os
from datetime import datetime
from typing import List

from app.core.event_bus import event_bus
from app.core.job_queue import job_queue
from app.core.registry import registry

from .autonomous_store import AutonomousStore


class AutonomousEngine:
    """Automatically run pipelines according to quotas."""

    name = "autonomous"

    def __init__(self) -> None:
        self.store = AutonomousStore()
        self.running = False
        self._task: asyncio.Task | None = None

    def initialize(self) -> dict:
        return {"status": "autonomous mode initialized"}

    def _project_files(self) -> List[str]:
        return [f for f in os.listdir(self.store.base) if f.endswith(".json")]

    async def auto_loop(self) -> None:
        """Core loop — checks projects and triggers pipelines."""
        self.running = True
        project_manager = registry.get_subsystem("project_manager")
        discovery = registry.get_subsystem("discovery")

        while self.running:
            project_ids = [int(name.split(".")[0]) for name in self._project_files()]
            for project_id in project_ids:
                state = self.store.reset_daily(project_id)
                if not state.get("auto_enabled"):
                    continue
                if state.get("clips_generated_today", 0) >= state.get("daily_quota", 1):
                    continue

                config = project_manager.get(project_id)
                creators = config.get("creators", [])
                if not creators:
                    continue

                new_posts = discovery.discover_for_project(project_id)
                if not new_posts:
                    await asyncio.sleep(1)
                    continue

                for link in new_posts:
                    job_queue.enqueue(
                        "download_url",
                        {"url": link, "project_id": project_id},
                    )

                state["last_run"] = datetime.utcnow().isoformat()
                state["clips_generated_today"] = state.get("clips_generated_today", 0) + len(new_posts)
                self.store.save_state(project_id, state)

                event_bus.publish(
                    "discovery_new_posts",
                    {"project_id": project_id, "new_posts": new_posts},
                )
                event_bus.publish(
                    "autonomous_pipeline_triggered",
                    {"project_id": project_id, "timestamp": state["last_run"]},
                )

            await asyncio.sleep(60)

    def start(self) -> None:
        if self._task and not self._task.done():
            return
        self._task = asyncio.create_task(self.auto_loop())

    def stop(self) -> None:
        self.running = False
        if self._task:
            self._task.cancel()
            self._task = None
