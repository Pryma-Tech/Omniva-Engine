"""Secure command router for operator actions."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/sanctum/sanctum_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/sanctum/sanctum_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/sanctum/sanctum_engine with cognitive telemetry.


from __future__ import annotations

from typing import Any, Dict

from app.sanctum.commands import COMMAND_TABLE


class SanctumEngine:
    """
    Secure command router for privileged operator actions.
    Accepts limited commands defined in COMMAND_TABLE.
    """

    def __init__(self, registry, commands) -> None:
        self.registry = registry
        self.commands = commands

    async def execute(self, command: str) -> Dict[str, Any]:
        if command not in COMMAND_TABLE:
            return {"ok": False, "error": "invalid_or_unauthorized_command"}

        method_name = COMMAND_TABLE[command]
        method = getattr(self.commands, method_name, None)

        if not method:
            return {"ok": False, "error": "command_missing_implementation"}

        try:
            result = await method()
            return {"ok": True, "result": result}
        except Exception as exc:  # pragma: no cover - defensive guard
            return {"ok": False, "error": str(exc)}
