"""Minimal autonomy loop adapter.

This is a simplified version of the omniva-v2 AutonomyKernel concept:
it tracks which projects are running, and exposes helpers so the
orchestrator can trigger micro/macro iterations in tests or via
future endpoints. It does NOT spawn background tasks here to keep
behavior deterministic for unit tests.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from app.core.event_bus import event_bus


class AutonomyAdapter:
    """Track running projects and expose micro/macro iterations."""

    def __init__(self, registry) -> None:
        self.registry = registry
        self.running: Dict[int, bool] = {}
        self.paused: Dict[int, bool] = {}

    def start_project(self, project_id: int) -> Dict[str, str]:
        if self.running.get(project_id):
            return {"status": "already_running"}
        self.running[project_id] = True
        self.paused[project_id] = False
        return {"status": "started"}

    def stop_project(self, project_id: int) -> Dict[str, str]:
        self.running[project_id] = False
        self.paused[project_id] = False
        return {"status": "stopped"}

    def pause_project(self, project_id: int) -> Dict[str, str]:
        if not self.running.get(project_id):
            return {"status": "not_running"}
        self.paused[project_id] = True
        return {"status": "paused"}

    def resume_project(self, project_id: int) -> Dict[str, str]:
        if not self.running.get(project_id):
            return {"status": "not_running"}
        self.paused[project_id] = False
        return {"status": "resumed"}

    def is_running(self, project_id: int) -> bool:
        return bool(self.running.get(project_id)) and not self.paused.get(project_id, False)

    # ------------------------------------------------------------------
    # Iteration helpers (called synchronously by tests or callers)
    # ------------------------------------------------------------------

    def run_micro_iteration(self, project_id: int) -> Dict[str, Any]:
        """Record a lightweight cognition/emotion snapshot."""
        intel = self.registry.get_subsystem("intelligence")
        if intel is None:
            return {"status": "intel_unavailable"}

        emotion = getattr(intel, "emotion_model", None)
        cognition = getattr(intel, "cognition", None)
        if emotion is None or cognition is None:
            return {"status": "intel_partial"}

        state = {
            "loop": "micro",
            "time": datetime.utcnow().isoformat(),
            "emotion": emotion.get(project_id),
            "attention": cognition.attention.get(project_id, 1.0),
        }
        cognition.push_memory(project_id, {"type": "autonomy_micro", **state})
        event_bus.publish("autonomy_micro_tick", {"project_id": project_id, **state})
        return {"status": "ok", **state}

    def run_macro_iteration(self, project_id: int) -> Dict[str, Any]:
        """Optionally ask the brain for a decision based on any available clips."""
        intel = self.registry.get_subsystem("intelligence")
        projects = self.registry.get_subsystem("project_manager")
        if intel is None or projects is None:
            return {"status": "intel_or_projects_unavailable"}

        clips: List[Dict[str, Any]] = []
        if hasattr(projects, "get_project_clips"):
            clips = projects.get_project_clips(project_id)

        decision: Dict[str, Any] | None = None
        if clips and hasattr(intel, "brain_decide"):
            decision = intel.brain_decide(project_id, clips)

        payload = {
            "loop": "macro",
            "time": datetime.utcnow().isoformat(),
            "decision": decision,
            "clips_considered": len(clips),
        }
        intel.cognition.push_memory(project_id, {"type": "autonomy_macro", **payload})
        event_bus.publish("autonomy_macro_tick", {"project_id": project_id, **payload})
        return {"status": "ok", **payload}

