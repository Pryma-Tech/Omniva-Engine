"""Heartbeat layer."""

from __future__ import annotations

import logging
from typing import Callable

from .heartbeat_engine import HeartbeatEngine
from .cron_tasks import CronTasks

__all__ = ["HeartbeatEngine", "CronTasks", "build_default_heartbeat"]


def build_default_heartbeat(registry, *, logger_factory: Callable[[str], logging.Logger] | None = None) -> HeartbeatEngine:
    """Construct a heartbeat engine wired to the provided registry."""
    logger_factory = logger_factory or logging.getLogger
    tasks = CronTasks(registry, logger=logger_factory("omniva.cron_tasks"))
    engine = HeartbeatEngine(
        registry,
        tasks,
        registry.config.heartbeat,
        logger=logger_factory("omniva.heartbeat"),
    )
    registry.heartbeat = engine
    registry.register("heartbeat", engine)
    return engine
