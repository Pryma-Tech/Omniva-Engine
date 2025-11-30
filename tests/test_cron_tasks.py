"""Unit tests for CronTasks behaviors."""

import asyncio

import pytest

from app.core.registry import build_registry
from app.heartbeat.cron_tasks import CronTasks


def test_midnight_reset_halves_high_drift():
    registry = build_registry()
    tasks = CronTasks(registry)
    projects = registry.get_subsystem("project_manager")
    intel = registry.get_subsystem("intelligence")
    project_ids = projects.get_all_project_ids()
    for pid in project_ids:
        intel.cognition.drift.state[pid]["drift_strength"] = 0.9

    result = asyncio.run(tasks.run_daily_midnight_reset())

    assert result["status"] == "midnight_reset_complete"
    for pid in project_ids:
        assert intel.cognition.drift.state[pid]["drift_strength"] == pytest.approx(0.45)


def test_keepalive_pushes_memory_entries():
    registry = build_registry()
    tasks = CronTasks(registry)
    intel = registry.get_subsystem("intelligence")
    projects = registry.get_subsystem("project_manager")
    project_ids = projects.get_all_project_ids()

    result = asyncio.run(tasks.send_agent_keepalive())

    assert result["status"] == "keepalive_sent"
    for pid in project_ids:
        assert len(intel.cognition.memory_log[pid]) == 1


def test_meta_learning_handles_missing_subsystem():
    registry = build_registry()
    tasks = CronTasks(registry)
    registry.register("meta", None)

    result = asyncio.run(tasks.run_daily_meta_learning())

    assert result["status"] == "meta_unavailable"

