"""Alignment and safety checks for agent actions."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/safety/safety_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/safety/safety_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/safety/safety_engine with cognitive telemetry.


from __future__ import annotations

from typing import Dict, Tuple


class SafetyEngine:
    """Ensure agent outputs respect project constraints."""

    def __init__(self, registry) -> None:
        self.registry = registry

    def validate_clip(self, project_id: int, clip: Dict) -> Tuple[bool, str | None]:
        if not clip:
            return False, "Missing clip payload"
        if "clip_id" not in clip:
            return False, "Missing clip_id"
        if clip.get("score", clip.get("priority", 0)) <= 0:
            return False, "Clip score too low"
        return True, None

    def validate_action(self, project_id: int, action: Dict) -> Tuple[bool, str | None]:
        clip_payload = action.get("chosen_clip") or action.get("final_choice") or action.get("chosen")
        ok, reason = self.validate_clip(project_id, clip_payload or {})
        if not ok:
            return False, reason
        projects = self.registry.get_subsystem("projects") or self.registry.get_subsystem("project_manager")
        if not projects:
            return False, "Project manager unavailable"
        config = getattr(projects, "get_project_config", getattr(projects, "get", None))
        cfg = config(project_id) if callable(config) else None
        if not cfg:
            return False, "Missing project configuration"
        # Placeholder for additional alignment rules (posting limits, schedule, etc.)
        return True, None
