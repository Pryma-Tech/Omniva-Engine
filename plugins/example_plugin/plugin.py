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
    # TODO(omniva-v0.1): Persist plugin events into Stardust for auditing.
    # TODO(omniva-v0.2): Add routing logic to trigger plugin-specific automations.
    # TODO(omniva-v0.3): Stream plugin events to the dashboard insight feed.
    _ = (event_name, payload)


def register_commands(commands) -> None:
    async def plugin_ping():
        return {"message": "example plugin pong"}

    commands.register_plugin_command("plugin.example.ping", plugin_ping)


def register_routes(router) -> None:
    @router.get("/example/status")
    async def example_status():
        # TODO(omniva-v0.1): Return real plugin diagnostics and heartbeat data.
        # TODO(omniva-v0.2): Surface plugin configuration/errors in response.
        return {"plugin": "example_plugin", "status": "active"}


def register_events(event_name: str, payload: Dict[str, Any]) -> None:
    """
    Default event hook invoked by the Forge engine.
    """
    if event_name == "plugin_example_event":
        # Future: trigger plugin-specific automation.
        # TODO(omniva-v0.1): Wire plugin_example_event to actual task handlers.
        # TODO(omniva-v0.2): Support additional event types and batching here.
        _ = payload
