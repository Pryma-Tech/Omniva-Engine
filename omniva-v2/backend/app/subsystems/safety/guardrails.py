"""Execution guardrails for safety-critical operations."""

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
