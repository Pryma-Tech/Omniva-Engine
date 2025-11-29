"""Safe operator command set for Sanctum."""

from __future__ import annotations

from typing import Any, Callable, Dict, List

import inspect

from app.core.event_bus import event_bus


class SanctumCommands:
    """
    Root-level operator commands.
    SAFE & LIMITED — NO arbitrary Python evaluation.
    """

    def __init__(self, registry) -> None:
        self.registry = registry
        self._plugin_command_index = 0

    def _projects(self):
        return (
            self.registry.get_subsystem("project_manager")
            or self.registry.get_subsystem("projects")
            or getattr(self.registry, "projects", None)
        )

    # SYSTEM COMMANDS
    async def heartbeat_restart(self) -> Dict[str, str]:
        self.registry.heartbeat.stop()
        self.registry.heartbeat.start()
        return {"message": "heartbeat restarted"}

    async def orchestrator_cycle(self) -> Dict[str, Any]:
        orch = self.registry.get_subsystem("orchestrator") or getattr(self.registry, "orchestrator", None)
        if not orch:
            return {"error": "orchestrator_unavailable"}
        return orch.global_cycle()

    async def recompute_identity(self) -> Dict[str, Any]:
        return self.registry.selfmodel.recompute_identity()

    async def flush_eventbus(self) -> Dict[str, Any]:
        # Event bus does not have a queue, but we can report history size.
        size = len(event_bus.get_log())
        return {"message": "eventbus has no queue — nothing to flush", "history_length": size}

    # INTROSPECTION COMMANDS
    async def show_identity(self) -> Dict[str, Any]:
        return self.registry.selfmodel.get_identity()

    async def show_insights(self) -> Dict[str, Any]:
        return self.registry.observatory.gather()

    async def show_epoch(self) -> Dict[str, Any]:
        archive = self.registry.archive
        return {
            "epoch": archive.current_epoch,
            "history_count": len(archive.timeline),
        }

    async def show_projects(self) -> List[int]:
        projects = self._projects()
        if not projects or not hasattr(projects, "get_all_project_ids"):
            return []
        return list(projects.get_all_project_ids())

    # DISCOVERY + WORKFLOWS
    async def run_discovery_all(self) -> Dict[str, Any]:
        disc = self.registry.get_subsystem("discovery") or getattr(self.registry, "discovery", None)
        if not disc or not hasattr(disc, "check_all_projects"):
            return {"error": "discovery_unavailable"}
        results = disc.check_all_projects()
        return {"discovery": results}

    def register_plugin_command(self, command_name: str, handler: Callable[[], Any]) -> Dict[str, str]:
        """
        Allow plugins to register additional Sanctum commands.
        """
        if not inspect.iscoroutinefunction(handler):
            raise ValueError("Plugin commands must be async functions")
        method_name = f"_plugin_command_{self._plugin_command_index}"
        self._plugin_command_index += 1
        setattr(self, method_name, handler)
        COMMAND_TABLE[command_name] = method_name
        return {"message": f"command {command_name} registered"}


COMMAND_TABLE = {
    "heartbeat.restart": "heartbeat_restart",
    "orchestrator.cycle": "orchestrator_cycle",
    "identity.recompute": "recompute_identity",
    "identity.show": "show_identity",
    "insights.show": "show_insights",
    "epoch.show": "show_epoch",
    "projects.show": "show_projects",
    "discovery.run_all": "run_discovery_all",
    "eventbus.flush": "flush_eventbus",
}
