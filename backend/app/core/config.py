"""Application configuration helpers and defaults."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable


def _float_env(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class HeartbeatConfig:
    orchestrator_interval: float = 600.0
    keepalive_interval: float = 120.0
    midnight_check_interval: float = 300.0
    loop_sleep_seconds: float = 1.0
    enable_logging: bool = True


@dataclass(frozen=True)
class AppConfig:
    heartbeat: HeartbeatConfig


def load_config_from_env() -> AppConfig:
    """Build the application config, honoring environment overrides."""
    hb = HeartbeatConfig(
        orchestrator_interval=_float_env("OMNIVA_HEARTBEAT_ORCH_INTERVAL", 600.0),
        keepalive_interval=_float_env("OMNIVA_HEARTBEAT_KEEPALIVE_INTERVAL", 120.0),
        midnight_check_interval=_float_env("OMNIVA_HEARTBEAT_MIDNIGHT_INTERVAL", 300.0),
        loop_sleep_seconds=_float_env("OMNIVA_HEARTBEAT_LOOP_SLEEP", 1.0),
        enable_logging=_bool_env("OMNIVA_HEARTBEAT_ENABLE_LOGGING", True),
    )
    return AppConfig(heartbeat=hb)

