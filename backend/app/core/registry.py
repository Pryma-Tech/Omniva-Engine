"""Subsystem registry plus lightweight stubs so APIs can execute."""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Iterable, List

from app.core.config import AppConfig, load_config_from_env
from app.heartbeat.cron_tasks import CronTasks
from app.heartbeat.heartbeat_engine import HeartbeatEngine
from app.subsystems.orchestrator.health_checks import HealthChecks
from app.subsystems.orchestrator.orchestrator_engine import MasterOrchestrator


class SubsystemRegistry:
    """Central registry shared across routers and subsystem stubs."""

    def __init__(self) -> None:
        self._subsystems: Dict[str, Any] = {}
        self.autonomy: AutonomyStub | None = None
        self.heartbeat: HeartbeatEngine | None = None
        self.orchestrator: MasterOrchestrator | None = None
        self.health: HealthChecks | None = None
        self.config: AppConfig | None = None

    def register(self, name: str, subsystem: Any) -> Any:
        """Store a subsystem instance under a canonical name."""
        self._subsystems[name] = subsystem
        return subsystem

    def get_subsystem(self, name: str) -> Any | None:
        """Retrieve a subsystem if registered."""
        return self._subsystems.get(name)


class ProjectManagerStub:
    """Minimal project registry powering orchestrator flows."""

    def __init__(self, project_ids: Iterable[str] | None = None) -> None:
        self._project_ids = list(project_ids or ("demo-project",))

    def get_all_project_ids(self) -> List[str]:
        return list(self._project_ids)


class DriftModelStub:
    """Simplified drift tracker used by CronTasks."""

    def __init__(self, project_ids: Iterable[str]) -> None:
        self.state: Dict[str, Dict[str, float]] = {
            pid: {"drift_strength": 0.4} for pid in project_ids
        }

    def get(self, pid: str) -> Dict[str, float]:
        return self.state.setdefault(pid, {"drift_strength": 0.2})


class CognitionStub:
    """Tracks working memory operations invoked by CronTasks."""

    def __init__(self, project_ids: Iterable[str]) -> None:
        project_ids = list(project_ids)
        self.drift = DriftModelStub(project_ids)
        self.memory_log: Dict[str, List[Dict[str, Any]]] = {pid: [] for pid in project_ids}

    def push_memory(self, pid: str, payload: Dict[str, Any]) -> None:
        self.memory_log.setdefault(pid, []).append(payload)


class IntelligenceStub:
    """Expose minimal intelligence surface for orchestrator + heartbeat."""

    def __init__(self, project_ids: Iterable[str]) -> None:
        self.cognition = CognitionStub(project_ids)


class AutonomyStub:
    """Records which projects are currently active."""

    def __init__(self) -> None:
        self.active_projects: set[str] = set()

    def start_project(self, pid: str) -> Dict[str, Any]:
        self.active_projects.add(pid)
        return {"project": pid, "status": "started"}

    def stop_project(self, pid: str) -> Dict[str, Any]:
        self.active_projects.discard(pid)
        return {"project": pid, "status": "stopped"}


class FederationStub:
    """Maintains shared heuristic state for reporting."""

    def __init__(self) -> None:
        self.shared_heuristics: Dict[str, float] = {}
        self.project_stats: Dict[str, Dict[str, float]] = {}

    def update_project_stats(self, pid: str) -> None:
        counter = len(self.project_stats) + 1
        self.project_stats[pid] = {"momentum": 0.75, "score": 0.5 + counter * 0.05}

    def federated_update(self) -> None:
        self.shared_heuristics = {
            pid: stats["score"] for pid, stats in self.project_stats.items()
        }


class MetaLearningStub:
    """Simple meta-learning loop tracker."""

    def __init__(self) -> None:
        self.iteration = 0

    def run_cycle(self) -> Dict[str, Any]:
        self.iteration += 1
        return {"iteration": self.iteration, "status": "ok"}


class PolicyModelStub:
    """Holds deterministic governance policies per project."""

    def __init__(self, project_ids: Iterable[str]) -> None:
        self._policies = {
            pid: {"posting_limit": 5, "strategy": "balanced"} for pid in project_ids
        }

    def get_policy(self, pid: str) -> Dict[str, Any]:
        return self._policies.setdefault(pid, {"posting_limit": 3, "strategy": "viral"})


class GovernanceStub:
    """Provides a policy_model accessor used by MasterOrchestrator."""

    def __init__(self, project_ids: Iterable[str]) -> None:
        self.policy_model = PolicyModelStub(project_ids)


class CrisisStub:
    """Placeholder for crisis management summaries."""

    def __init__(self) -> None:
        self.recent_events: List[Dict[str, Any]] = []


def _build_registry(
    config: AppConfig | None = None,
    *,
    logger_factory: Callable[[str], logging.Logger] | None = None,
) -> SubsystemRegistry:
    registry = SubsystemRegistry()
    registry.config = config or load_config_from_env()
    log_factory = logger_factory or (lambda name: logging.getLogger(name))

    projects = registry.register("project_manager", ProjectManagerStub())
    # Keep backward-compatible alias for legacy lookups.
    registry.register("projects", projects)

    intelligence = registry.register("intelligence", IntelligenceStub(projects.get_all_project_ids()))
    autonomy = AutonomyStub()
    registry.autonomy = autonomy

    federation = registry.register("federation", FederationStub())
    meta = registry.register("meta", MetaLearningStub())
    governance = registry.register("governance", GovernanceStub(projects.get_all_project_ids()))
    registry.register("crisis", CrisisStub())

    cron_tasks = CronTasks(registry, logger=log_factory("omniva.cron_tasks"))
    heartbeat = HeartbeatEngine(
        registry,
        cron_tasks,
        registry.config.heartbeat,
        logger=log_factory("omniva.heartbeat"),
    )
    registry.heartbeat = heartbeat

    health_checks = HealthChecks(registry)
    registry.health = health_checks

    orchestrator = MasterOrchestrator(registry, health_checks)
    registry.orchestrator = orchestrator
    registry.register("orchestrator", orchestrator)

    registry.register("autonomy", autonomy)
    registry.register("heartbeat", heartbeat)

    # Ensure meta + governance subsystems are retained for lookups.
    registry.register("intelligence_cognition", intelligence.cognition)

    return registry


def build_registry(
    config: AppConfig | None = None,
    *,
    logger_factory: Callable[[str], logging.Logger] | None = None,
) -> SubsystemRegistry:
    """Factory for creating new registry instances (useful in tests)."""
    return _build_registry(config, logger_factory=logger_factory)


registry = _build_registry()
