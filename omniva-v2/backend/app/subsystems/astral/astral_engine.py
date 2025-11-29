"""Master multi-world futures module."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/astral/astral_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/astral/astral_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/astral/astral_engine with cognitive telemetry.


from __future__ import annotations

from typing import Dict, List


class AstralEngine:
    """
    Combines:
      - TimelineSimulator
      - ScenarioEngine
      - Oracle forecasts
      - Multi-world timeline synthesis
    """

    def __init__(self, registry, simulator, scenarios) -> None:
        self.registry = registry
        self.sim = simulator
        self.scenarios = scenarios

    def _project_ids(self) -> List[int]:
        projects = (
            self.registry.get_subsystem("project_manager")
            or self.registry.get_subsystem("projects")
            or getattr(self.registry, "projects", None)
        )
        if projects and hasattr(projects, "get_all_project_ids"):
            return list(projects.get_all_project_ids())
        return []

    def compute_initial_state(self, project_id: int) -> Dict[str, float]:
        """
        Build the initial state using Oracle's most recent forecasts.
        """
        forecast = self.registry.oracle.project_forecast(project_id)
        return {
            "drift": forecast["drift"]["expected"],
            "stress": forecast["stress"]["expected"],
            "trend": forecast["trend"]["expected"],
        }

    def alternate_futures(self, project_id: int) -> Dict[str, object]:
        initial_state = self.compute_initial_state(project_id)
        future_branches = self.scenarios.run_scenarios(initial_state)
        return {
            "project_id": project_id,
            "initial": initial_state,
            "branches": future_branches,
        }

    def astral_snapshot(self) -> Dict[str, object]:
        """
        Generate multi-world snapshot for all projects.
        """
        projects = self._project_ids()
        return {
            "projects": {pid: self.alternate_futures(pid) for pid in projects},
            "epoch": self.registry.archive.current_epoch,
            "identity": self.registry.selfmodel.get_identity(),
        }
