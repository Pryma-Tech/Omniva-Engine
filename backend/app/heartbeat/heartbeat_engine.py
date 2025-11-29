"""Global async scheduler for Omniva."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Tuple


class HeartbeatEngine:
    """Manage CRON-like schedules and keepalive signals."""

    def __init__(self, registry, tasks) -> None:
        self.registry = registry
        self.tasks = tasks
        self.running = False
        self.last_midnight = None
        self._loop_task: asyncio.Task | None = None

    def start(self) -> dict:
        # TODO(omniva-v0.1): Validate registry prerequisites before toggling heartbeat.
        # TODO(omniva-v0.2): Support specifying custom intervals via payload/config.
        if self.running:
            return {"status": "already_running"}
        self.running = True
        self._loop_task = asyncio.create_task(self.run_loop())
        return {"status": "heartbeat_started"}

    def stop(self) -> dict:
        # TODO(omniva-v0.1): Flush pending tasks before stopping heartbeat loop.
        self.running = False
        if self._loop_task:
            self._loop_task.cancel()
            self._loop_task = None
        return {"status": "heartbeat_stopped"}

    async def run_loop(self) -> None:
        # TODO(omniva-v0.1): Replace hard-coded intervals with configuration values.
        # TODO(omniva-v0.2): Add structured logging/metrics for each loop iteration.
        # TODO(omniva-v0.3): Allow pluggable scheduling policies (cron expressions).
        orch_interval = 10 * 60  # 10 minutes
        keepalive_interval = 2 * 60  # 2 minutes
        last_orch = datetime.utcnow()
        last_keep = datetime.utcnow()
        self.last_midnight = datetime.utcnow().date()
        while self.running:
            now = datetime.utcnow()
            if now.date() != self.last_midnight:
                await self.tasks.run_daily_midnight_reset()
                await self.tasks.run_daily_meta_learning()
                self.last_midnight = now.date()
            if (now - last_orch).total_seconds() >= orch_interval:
                await self.tasks.run_periodic_orchestration_cycle()
                last_orch = now
            if (now - last_keep).total_seconds() >= keepalive_interval:
                await self.tasks.send_agent_keepalive()
                last_keep = now
            await asyncio.sleep(1)
