"""Core primitives and subsystem wiring for Omniva Engine v2."""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/core/__init__ with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/core/__init__ with cognitive telemetry.

from .config import Config, as_dict, load_config  # noqa: F401

__all__ = ["Config", "as_dict", "load_config"]
