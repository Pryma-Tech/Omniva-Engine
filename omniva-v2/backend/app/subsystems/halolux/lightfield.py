"""Unified cross-system interpretability fabric for HaloLux."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/halolux/lightfield.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/halolux/lightfield with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/halolux/lightfield with cognitive telemetry.


from __future__ import annotations

from typing import Dict


class HaloLightfield:
    """Captures snapshots across major subsystems."""

    def __init__(self, registry) -> None:
        self.registry = registry

    def capture_state(self) -> Dict[str, object]:
        projects = (
            self.registry.get_subsystem("project_manager")
            or self.registry.get_subsystem("projects")
            or getattr(self.registry, "projects", None)
        )
        project_ids = projects.get_all_project_ids() if projects and hasattr(projects, "get_all_project_ids") else []
        return {
            "pantheon": self.registry.pantheon.pantheon_snapshot(),
            "chorus": self.registry.chorus.chorus_snapshot(),
            "horizon": self.registry.horizon.horizon_snapshot(),
            "oracle": self.registry.oracle.system_summary(),
            "astral": {pid: self.registry.astral.alternate_futures(pid) for pid in project_ids},
            "strategy": self.registry.strategy.global_summary(),
            "infinity": self.registry.infinity.infinity_snapshot(),
            "paradox": self.registry.paradox.paradox_snapshot(),
            "eclipse": self.registry.eclipse.eclipse_snapshot(),
            "lattice": self.registry.lattice.lattice_snapshot(),
            "stardust": self.registry.stardust.graph_snapshot(),
        }
