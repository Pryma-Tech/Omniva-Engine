"""Unit tests for the HeartbeatEngine scheduler logic."""

from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock

import logging

from app.core.config import HeartbeatConfig
from app.heartbeat.heartbeat_engine import HeartbeatEngine


def _build_engine(**overrides):
    config = HeartbeatConfig(
        orchestrator_interval=overrides.get("orchestrator_interval", 30),
        keepalive_interval=overrides.get("keepalive_interval", 10),
        midnight_check_interval=overrides.get("midnight_check_interval", 5),
        loop_sleep_seconds=overrides.get("loop_sleep_seconds", 0.01),
        enable_logging=False,
    )
    tasks = SimpleNamespace(
        run_daily_midnight_reset=AsyncMock(return_value={"status": "ok"}),
        run_daily_meta_learning=AsyncMock(return_value={"status": "ok"}),
        run_periodic_orchestration_cycle=AsyncMock(return_value={"status": "ok"}),
        send_agent_keepalive=AsyncMock(return_value={"status": "ok"}),
    )
    registry = SimpleNamespace()
    engine = HeartbeatEngine(registry, tasks, config, logger=logging.getLogger("test.heartbeat"))
    return engine, tasks, config


def test_tick_triggers_keepalive_after_interval():
    engine, tasks, config = _build_engine()
    start = datetime(2025, 1, 1, 0, 0, 0)

    assert engine.tick(start) == []

    actions = engine.tick(start + timedelta(seconds=config.keepalive_interval))

    assert "agent_keepalive" in actions
    assert tasks.send_agent_keepalive.await_count == 1


def test_tick_runs_midnight_reset_once_per_day():
    engine, tasks, config = _build_engine(midnight_check_interval=1)
    start = datetime(2025, 1, 1, 23, 59, 0)

    engine.tick(start)
    actions = engine.tick(start + timedelta(minutes=2))

    assert "midnight_reset" in actions
    assert "meta_learning" in actions
    assert tasks.run_daily_midnight_reset.await_count == 1
    assert tasks.run_daily_meta_learning.await_count == 1


def test_tick_runs_orchestration_cycle_on_interval():
    engine, tasks, config = _build_engine(orchestrator_interval=15)
    start = datetime(2025, 1, 1, 0, 0, 0)

    engine.tick(start)
    actions = engine.tick(start + timedelta(seconds=config.orchestrator_interval))

    assert "orchestration_cycle" in actions
    assert tasks.run_periodic_orchestration_cycle.await_count == 1

