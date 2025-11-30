"""Execution guardrails for safety-critical operations."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/safety/guardrails.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/safety/guardrails with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/safety/guardrails with cognitive telemetry.


from __future__ import annotations

import traceback
from typing import Awaitable


class GuardrailEngine:
    """Wrap coroutine execution with crisis handling."""

    def __init__(self, registry) -> None:
        self.registry = registry

    async def safe_call(self, project_id: int, coro: Awaitable, label: str):
        try:
            return await coro
        except Exception as exc:  # pylint: disable=broad-except
            crisis = self.registry.crisis
            crisis.handle_exception(project_id, label, exc, traceback.format_exc())
            return None
