"""Global async scheduler for Omniva."""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Awaitable, Callable, Dict, List

from app.core.config import HeartbeatConfig


class HeartbeatEngine:
    """Manage CRON-like schedules and keepalive signals."""

    def __init__(self, registry, tasks, config: HeartbeatConfig, logger: logging.Logger | None = None) -> None:
        self.registry = registry
        self.tasks = tasks
        self.config = config
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
        drained: List[str] = []
        if self._loop_task:
            loop = None
            try:
                loop = self._loop_task.get_loop()
            except Exception:
                pass
            try:
                if loop and loop is not asyncio.get_running_loop():
                    self._loop_task.cancel()
                else:
                    await asyncio.wait_for(self._loop_task, timeout=getattr(self.config, "shutdown_timeout", 5.0))
            except asyncio.TimeoutError:
                self.logger.warning("heartbeat.stop_timeout")
                self._loop_task.cancel()
            finally:
                self._loop_task = None
        # Run a final iteration to flush any pending cron tasks.
        drained = await self._process_iteration(datetime.utcnow())
        payload = {"status": "heartbeat_stopped", "drained_actions": drained}
        self.logger.info("heartbeat.stop", extra=payload)
        return payload

    def tick(self, now: datetime) -> List[str]:
        """Run a single scheduler iteration (mostly for deterministic tests)."""
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
        except Exception:
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
        if (now - self._last_midnight_check).total_seconds() >= self.config.midnight_check_interval:
            self._last_midnight_check = now
            return True
        return False

    @staticmethod
    def _elapsed(now: datetime, previous: datetime | None, interval_seconds: float) -> bool:
        if previous is None:
            return True
        return (now - previous).total_seconds() >= interval_seconds

    def _missing_prerequisites(self) -> List[str]:
        missing = []
        for name in self._prerequisites:
            if not self.registry.get_subsystem(name):
                missing.append(name)
        return missing

    def schedule_snapshot(self) -> Dict[str, Dict[str, str | None] | bool]:
        """Expose last/next timestamps so the API can report scheduler state."""
        return {
            "running": self.running,
            "last": {
                "midnight_reset": self._dt_to_str(self._last_midnight_check),
                "orchestration_cycle": self._dt_to_str(self._last_orchestration),
                "agent_keepalive": self._dt_to_str(self._last_keepalive),
            },
            "next": {
                "orchestration_cycle": self._next_run(self._last_orchestration, self.config.orchestrator_interval),
                "agent_keepalive": self._next_run(self._last_keepalive, self.config.keepalive_interval),
            },
        }

    @staticmethod
    def _dt_to_str(value: datetime | None) -> str | None:
        return value.isoformat() if value else None

    @staticmethod
    def _next_run(last: datetime | None, interval_seconds: float) -> str | None:
        if last is None:
            return None
        return (last + timedelta(seconds=interval_seconds)).isoformat()
