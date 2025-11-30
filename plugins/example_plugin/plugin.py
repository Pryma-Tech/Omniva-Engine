"""Example plugin showcasing Omniva Forge hooks."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from app.core.event_bus import event_bus
from app.core.registry import registry

EVENT_DIR = Path("backend/storage/plugins")
EVENT_LOG = EVENT_DIR / "example_events.jsonl"


def init(registry) -> None:
    """Run during plugin enablement."""
    bus = getattr(registry, "eventbus", None) or event_bus
    bus.register_plugin_hook(plugin_event_logger)


def plugin_event_logger(event_name: str, payload: Dict[str, Any]) -> None:
    """
    Sample event observer used to demonstrate the hook system.
    Persists every observed event to a JSONL log for later diagnostics.
    """
    record = {
        "event": event_name,
        "payload": payload,
        "timestamp": datetime.utcnow().isoformat(),
    }
    _persist_event(record)


def register_commands(commands) -> None:
    async def plugin_ping():
        return {"message": "example plugin pong", "timestamp": datetime.utcnow().isoformat()}

    commands.register_plugin_command("plugin.example.ping", plugin_ping)


def register_routes(router) -> None:
    @router.get("/example/status")
    async def example_status():
        heartbeat = getattr(registry, "heartbeat", None)
        return {
            "plugin": "example_plugin",
            "status": "active",
            "heartbeat_running": heartbeat.running if heartbeat else False,
            "recent_events": _load_recent_events(),
        }


def register_events(event_name: str, payload: Dict[str, Any]) -> None:
    """
    Default event hook invoked by the Forge engine.
    """
    if event_name != "plugin_example_event":
        return
    plugin_event_logger(event_name, payload)
    project_id = payload.get("project_id")
    autonomy = getattr(registry, "autonomy", None)
    if project_id and autonomy:
        autonomy.run_micro_iteration(int(project_id))


def _persist_event(record: Dict[str, Any]) -> None:
    EVENT_DIR.mkdir(parents=True, exist_ok=True)
    with EVENT_LOG.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record) + "\n")
    _truncate_log()


def _load_recent_events(limit: int = 10) -> List[Dict[str, Any]]:
    if not EVENT_LOG.exists():
        return []
    events: List[Dict[str, Any]] = []
    with EVENT_LOG.open("r", encoding="utf-8") as handle:
        for line in handle.readlines()[-limit:]:
            try:
                events.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue
    return events


def _truncate_log(max_entries: int = 200) -> None:
    if not EVENT_LOG.exists():
        return
    with EVENT_LOG.open("r", encoding="utf-8") as handle:
        lines = handle.readlines()
    if len(lines) <= max_entries:
        return
    with EVENT_LOG.open("w", encoding="utf-8") as handle:
        handle.writelines(lines[-max_entries:])
