"""Subsystem registry plus lightweight stubs so APIs can execute."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Callable, Dict, Iterable, List

from app.core.config import AppConfig, load_config_from_env
from app.core.event_bus import event_bus
from app.heartbeat.cron_tasks import CronTasks
from app.heartbeat.heartbeat_engine import HeartbeatEngine
from app.subsystems.autonomy import AutonomyAdapter
from app.subsystems.horizon import HorizonStore
from app.subsystems.orchestrator.health_checks import HealthChecks
from app.subsystems.projects import ProjectManager
from app.subsystems.scheduler import SchedulerSubsystem
from app.subsystems.orchestrator.orchestrator_engine import MasterOrchestrator


class SubsystemRegistry:
    """Central registry shared across routers and subsystem stubs."""

    def __init__(self) -> None:
        self._subsystems: Dict[str, Any] = {}
        self.autonomy: Any | None = None
        self.eventbus = None
        self.heartbeat: HeartbeatEngine | None = None
        self.orchestrator: MasterOrchestrator | None = None
        self.health: HealthChecks | None = None
        self.config: AppConfig | None = None
        self.projects: ProjectManager | None = None

    def register(self, name: str, subsystem: Any) -> Any:
        """Store a subsystem instance under a canonical name."""
        self._subsystems[name] = subsystem
        return subsystem

    def get_subsystem(self, name: str) -> Any | None:
        """Retrieve a subsystem if registered."""
        return self._subsystems.get(name)


class ProjectManagerStub:
    """Minimal project registry powering orchestrator flows."""

    def __init__(self, project_ids: Iterable[int] | None = None) -> None:
        self._project_ids = [int(pid) for pid in (project_ids or (1,))]

    def get_all_project_ids(self) -> List[int]:
        return list(self._project_ids)


class DriftModelStub:
    """Simplified drift tracker used by CronTasks."""

    def __init__(self, project_ids: Iterable[int]) -> None:
        self.state: Dict[int, Dict[str, float]] = {
            pid: {"drift_strength": 0.4} for pid in project_ids
        }

    def get(self, pid: int) -> Dict[str, float]:
        return self.state.setdefault(pid, {"drift_strength": 0.2})


class CognitionStub:
    """Tracks working memory operations invoked by CronTasks."""

    def __init__(self, project_ids: Iterable[str]) -> None:
        project_ids = [int(pid) for pid in project_ids]
        self.drift = DriftModelStub(project_ids)
        self.memory_log: Dict[int, List[Dict[str, Any]]] = {pid: [] for pid in project_ids}
        self.attention: Dict[int, float] = {pid: 1.0 for pid in project_ids}

    def push_memory(self, pid: int, payload: Dict[str, Any]) -> None:
        log = self.memory_log.setdefault(pid, [])
        log.append(payload)
        # Keep the log bounded so diagnostics stay small.
        if len(log) > 200:
            del log[:-200]

    def recent_memory(self, pid: int, limit: int = 10) -> List[Dict[str, Any]]:
        return list(self.memory_log.get(pid, [])[-limit:])

    def update_attention(self, pid: int, value: float) -> None:
        self.attention[pid] = max(0.0, min(1.0, value))


class EmotionModelStub:
    """Provides lightweight stress/confidence tracking."""

    def __init__(self, project_ids: Iterable[str]) -> None:
        self._state: Dict[int, Dict[str, float]] = {
            int(pid): {"stress": 0.25, "confidence": 0.7} for pid in project_ids
        }

    def get(self, pid: int) -> Dict[str, float]:
        return self._state.setdefault(int(pid), {"stress": 0.3, "confidence": 0.6})

    def adjust(self, pid: int, *, stress_delta: float = 0.0, confidence_delta: float = 0.0) -> Dict[str, float]:
        state = self.get(pid)
        state["stress"] = max(0.0, min(1.0, state["stress"] + stress_delta))
        state["confidence"] = max(0.0, min(1.0, state["confidence"] + confidence_delta))
        return state


class IntelligenceStub:
    """Expose minimal intelligence surface for orchestrator + heartbeat."""

    def __init__(self, project_ids: Iterable[str]) -> None:
        self.cognition = CognitionStub(project_ids)
        self.emotion_model = EmotionModelStub(project_ids)


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

    def record(self, project_id: int, description: str) -> None:
        self.recent_events.append(
            {
                "project_id": int(project_id),
                "description": description,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    def get_crises(self, project_id: int) -> List[Dict[str, Any]]:
        target = int(project_id)
        return [evt for evt in self.recent_events if evt.get("project_id") == target]


def _build_registry(
    config: AppConfig | None = None,
    *,
    logger_factory: Callable[[str], logging.Logger] | None = None,
) -> SubsystemRegistry:
    registry = SubsystemRegistry()
    registry.config = config or load_config_from_env()
    log_factory = logger_factory or (lambda name: logging.getLogger(name))

    # Real project manager backed by JSON store.
    projects = registry.register("project_manager", ProjectManager())
    # Keep backward-compatible alias for legacy lookups.
    registry.register("projects", projects)
    registry.projects = projects

    intelligence = registry.register("intelligence", IntelligenceStub(projects.get_all_project_ids()))
    registry.register("event_bus", event_bus)
    registry.eventbus = event_bus

    # Autonomy adapter for per-project loops.
    autonomy = AutonomyAdapter(registry)
    registry.autonomy = autonomy
    registry.register("autonomy", autonomy)

    # Minimal scheduler + horizon stubs.
    scheduler = SchedulerSubsystem()
    registry.register("scheduler", scheduler)
    horizon = HorizonStore()
    registry.register("horizon", horizon)

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

    registry.register("heartbeat", heartbeat)

    # Ensure meta + governance subsystems are retained for lookups.
    registry.register("intelligence_cognition", intelligence.cognition)

    registry.eventbus = event_bus

    return registry


def build_registry(
    config: AppConfig | None = None,
    *,
    logger_factory: Callable[[str], logging.Logger] | None = None,
) -> SubsystemRegistry:
    """Factory for creating new registry instances (useful in tests)."""
    return _build_registry(config, logger_factory=logger_factory)


registry = _build_registry()
