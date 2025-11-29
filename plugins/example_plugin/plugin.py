"""Example plugin showcasing Omniva Forge hooks."""

from __future__ import annotations

from typing import Any, Dict


def init(registry) -> None:
    """Run during plugin enablement."""
    registry.eventbus.register_plugin_hook(plugin_event_logger)


async def plugin_event_logger(event_name: str, payload: Dict[str, Any]) -> None:
    """
    Sample event observer used to demonstrate the hook system.
    Currently a no-op placeholder to keep the example lightweight.
    """
    _ = (event_name, payload)


def register_commands(commands) -> None:
    async def plugin_ping():
        return {"message": "example plugin pong"}

    commands.register_plugin_command("plugin.example.ping", plugin_ping)


def register_routes(router) -> None:
    @router.get("/example/status")
    async def example_status():
        return {"plugin": "example_plugin", "status": "active"}


def register_events(event_name: str, payload: Dict[str, Any]) -> None:
    """
    Default event hook invoked by the Forge engine.
    """
    if event_name == "plugin_example_event":
        # Future: trigger plugin-specific automation.
        _ = payload
