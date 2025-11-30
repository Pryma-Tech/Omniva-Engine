"""Configuration loader for Omniva Engine v2.

This v0.1 implementation reads from environment variables and exposes a
frozen dataclass instance used throughout the backend.
"""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/core/config with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/core/config with cognitive telemetry.

# TODO: Load from YAML/env and validate schema.

import os
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Config:
    """Core configuration options."""

    app_name: str = "Omniva Engine v2"
    environment: str = "development"
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    next_public_backend_url: str = "http://localhost:8000"
    database_url: str = "sqlite:///storage/omniva.db"
    database_echo: bool = False


CONFIG = Config(
    app_name=os.getenv("OMNIVA_APP_NAME", "Omniva Engine v2"),
    environment=os.getenv("OMNIVA_ENV", "development"),
    backend_host=os.getenv("BACKEND_HOST", "0.0.0.0"),
    backend_port=int(os.getenv("BACKEND_PORT", "8000")),
    next_public_backend_url=os.getenv("NEXT_PUBLIC_BACKEND_URL", "http://localhost:8000"),
    database_url=os.getenv("DATABASE_URL", "sqlite:///storage/omniva.db"),
    database_echo=os.getenv("DATABASE_ECHO", "false").lower() in {"1", "true", "yes"},
)


def load_config() -> Config:
    """Return cached config object."""
    return CONFIG


def as_dict() -> Dict[str, Any]:
    """Expose config as simple dict for responses."""
    return CONFIG.__dict__.copy()
