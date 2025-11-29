"""Behavior tree execution engine."""

from __future__ import annotations

from typing import Any, Dict

from app.core.registry import registry

from .project_trees import get_project_tree


class BehaviorTreeEngine:
    """Executes behavior trees for each project."""

    def run(self, project_id: int, ctx: Dict[str, Any]) -> Dict[str, Any]:
        ctx = ctx or {}
        ctx.setdefault("project", {"id": project_id})
        ctx.setdefault("trace", [])
        intel = registry.get_subsystem("intelligence")
        if intel:
            persona_profile = intel.persona.get_persona(project_id)
            ctx.setdefault("persona_profile", persona_profile)
            temperament = intel.persona.temperaments.get(persona_profile["temperament"], {})
            ctx.setdefault("persona_tone", temperament.get("tone"))
        tree = get_project_tree(project_id)
        success = bool(tree.tick(ctx))
        return {"project_id": project_id, "success": success, "context": ctx}
