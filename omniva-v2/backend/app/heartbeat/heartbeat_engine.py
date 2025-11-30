"""Global async scheduler for Omniva (v2 heartbeat engine).

This is a lightly adapted copy of the legacy heartbeat engine with a
compatible API plus a relaxed constructor that can operate without an
explicit config object. When ``config`` is omitted, sensible defaults
are used so callers like the v2 registry can simply do::

    HeartbeatEngine(registry, cron_tasks)
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Awaitable, Callable, Dict, List, Optional


@dataclass
class HeartbeatConfig:
    """Lightweight configuration for the heartbeat loop."""

    orchestrator_interval: float = 600.0
    keepalive_interval: float = 120.0
    midnight_check_interval: float = 300.0
    loop_sleep_seconds: float = 1.0
    enable_logging: bool = True
    shutdown_timeout: float = 5.0


class HeartbeatEngine:
    """Manage CRON-like schedules and keepalive signals."""

    def __init__(
        self,
        registry,
        tasks,
        config: Optional[HeartbeatConfig] = None,
        logger: logging.Logger | None = None,
    ) -> None:
        self.registry = registry
        self.tasks = tasks
        self.config = config or HeartbeatConfig()
        self.logger = logger or logging.getLogger(__name__)
        self.running = False
        self.last_midnight = None
        self._last_midnight_check = None
        self._last_orchestration = None
        self._last_keepalive = None
        self._loop_task: asyncio.Task | None = None
        self._prerequisites = ("project_manager", "intelligence", "orchestrator")

    def start(self) -> dict:
        if self.running:
            return {"status": "already_running"}
        missing = self._missing_prerequisites()
        if missing:
            payload = {"status": "unavailable", "missing": missing}
            self.logger.warning("heartbeat.start_blocked", extra=payload)
            return payload
        self.running = True
        now = datetime.utcnow()
        self._initialize_clocks(now)
        self.logger.info("heartbeat.start", extra={"status": "started"})
        self._loop_task = asyncio.create_task(self.run_loop())
        return {"status": "heartbeat_started", "schedule": self.schedule_snapshot()}

    async def stop(self) -> dict:
        if not self.running:
            return {"status": "not_running"}
        self.running = False
        if self._loop_task:
            try:
                await asyncio.wait_for(self._loop_task, timeout=self.config.shutdown_timeout)
            except asyncio.TimeoutError:
                self.logger.warning("heartbeat.stop_timeout")
                self._loop_task.cancel()
            finally:
                self._loop_task = None
        drained = await self._process_iteration(datetime.utcnow())
        payload = {"status": "heartbeat_stopped", "drained_actions": drained}
        self.logger.info("heartbeat.stop", extra=payload)
        return payload

    def tick(self, now: datetime) -> List[str]:
        """Run a single scheduler iteration (primarily for tests)."""
        self._ensure_initialized(now)
        return asyncio.run(self._process_iteration(now))

    async def run_loop(self) -> None:
        """Continuous scheduler loop executed when heartbeat is running."""
        while self.running:
            now = datetime.utcnow()
            await self._process_iteration(now)
            await asyncio.sleep(self.config.loop_sleep_seconds)

    async def _process_iteration(self, now: datetime) -> List[str]:
        self._ensure_initialized(now)
        actions: List[str] = []

        if self._should_check_midnight(now) and now.date() != self.last_midnight:
            await self._run_action("midnight_reset", self.tasks.run_daily_midnight_reset)
            await self._run_action("meta_learning", self.tasks.run_daily_meta_learning)
            self.last_midnight = now.date()
            actions.extend(["midnight_reset", "meta_learning"])

        if self._elapsed(now, self._last_orchestration, self.config.orchestrator_interval):
            await self._run_action("orchestration_cycle", self.tasks.run_periodic_orchestration_cycle)
            self._last_orchestration = now
            actions.append("orchestration_cycle")

        if self._elapsed(now, self._last_keepalive, self.config.keepalive_interval):
            await self._run_action("agent_keepalive", self.tasks.send_agent_keepalive)
            self._last_keepalive = now
            actions.append("agent_keepalive")

        return actions

    async def _run_action(self, label: str, action: Callable[[], Awaitable[dict]]) -> None:
        try:
            result = await action()
            if self.config.enable_logging:
                self.logger.info("heartbeat.%s", label, extra={"action": label, "result": result})
        except Exception:  # pragma: no cover - defensive logging
            self.logger.exception("heartbeat.%s failed", label)

    def _initialize_clocks(self, now: datetime) -> None:
        self.last_midnight = now.date()
        self._last_midnight_check = now
        self._last_orchestration = now
        self._last_keepalive = now

    def _ensure_initialized(self, now: datetime) -> None:
        if self._last_orchestration is None or self._last_keepalive is None:
            self._initialize_clocks(now)

    def _should_check_midnight(self, now: datetime) -> bool:
        if self._last_midnight_check is None:
            self._last_midnight_check = now
            return True
        if (now - self._last_midnight_check) >= timedelta(seconds=self.config.midnight_check_interval):
            self._last_midnight_check = now
            return True
        return False

    @staticmethod
    def _elapsed(now: datetime, last: Optional[datetime], interval: float) -> bool:
        if last is None:
            return True
        return (now - last) >= timedelta(seconds=interval)

    def _missing_prerequisites(self) -> List[str]:
        missing: List[str] = []
        for name in self._prerequisites:
            if self.registry.get_subsystem(name) is None and not hasattr(self.registry, name):
                missing.append(name)
        return missing

    def schedule_snapshot(self) -> Dict[str, object]:
        return {
            "orchestrator_interval": self.config.orchestrator_interval,
            "keepalive_interval": self.config.keepalive_interval,
            "midnight_check_interval": self.config.midnight_check_interval,
            "running": self.running,
        }

