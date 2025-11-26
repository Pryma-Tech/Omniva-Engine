"""Subsystem registry (placeholder)."""
# TODO: Add lifecycle management and plugin discovery.

from typing import Any, Dict

import logging

logger = logging.getLogger("omniva_v2")


class SubsystemRegistry:
    """Simple in-memory registry for subsystem instances."""

    def __init__(self):
        self._registry: Dict[str, Any] = {}
        logger.info("SubsystemRegistry initialized (placeholder).")

    def register_subsystem(self, name: str, instance: Any) -> None:
        logger.info("Registering subsystem %s (placeholder)", name)
        self._registry[name] = instance

    def get_subsystem(self, name: str) -> Any:
        return self._registry.get(name)

    def list_subsystems(self) -> Dict[str, str]:
        return {name: instance.__class__.__name__ for name, instance in self._registry.items()}


REGISTRY = SubsystemRegistry()


def register_subsystem(name: str, instance: Any) -> None:
    REGISTRY.register_subsystem(name, instance)


def get_subsystem(name: str) -> Any:
    return REGISTRY.get_subsystem(name)


def list_subsystems() -> Dict[str, str]:
    return REGISTRY.list_subsystems()

registry = REGISTRY


def initialize_all():
    """Call initialize on all registered subsystems if available."""
    for subsystem in REGISTRY._registry.values():
        if hasattr(subsystem, "initialize"):
            subsystem.initialize()
