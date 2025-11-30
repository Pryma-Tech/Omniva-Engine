"""Master orchestrator subsystem."""

from __future__ import annotations

from typing import Callable

from .orchestrator_engine import MasterOrchestrator
from .health_checks import HealthChecks

__all__ = ["MasterOrchestrator", "HealthChecks", "build_orchestrator"]


def build_orchestrator(registry, *, logger_factory: Callable[[str], object] | None = None) -> MasterOrchestrator:
    """Wire up the orchestrator, registering health checks automatically."""
    health = HealthChecks(registry)
    registry.health = health
    orchestrator = MasterOrchestrator(registry, health)
    registry.orchestrator = orchestrator
    registry.register("orchestrator", orchestrator)
    return orchestrator
