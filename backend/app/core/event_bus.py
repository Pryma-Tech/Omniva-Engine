"""Minimal asynchronous event bus for the v0.1 backend."""

from __future__ import annotations

import asyncio
import inspect
from collections import defaultdict, deque
from datetime import datetime
from typing import Any, Awaitable, Callable, DefaultDict, Deque, Dict, List

AsyncHandler = Callable[[Dict[str, Any]], Awaitable[None]]
PluginHook = Callable[[str, Dict[str, Any]], Any]


class EventBus:
    """Simple pub/sub hub with an in-memory rolling log."""

    def __init__(self, max_log_entries: int = 500) -> None:
        self._subscribers: DefaultDict[str, List[AsyncHandler]] = defaultdict(list)
        self._log: Deque[Dict[str, Any]] = deque(maxlen=max_log_entries)
        self._lock = asyncio.Lock()
        self._plugin_hooks: List[PluginHook] = []

    def subscribe(self, event_name: str, handler: AsyncHandler) -> None:
        """Register an async handler for an event."""
        self._subscribers[event_name].append(handler)

    async def publish_async(self, event_name: str, payload: Dict[str, Any]) -> None:
        """Record and dispatch an event to all subscribers."""
        async with self._lock:
            self._log.append(
                {
                    "event": event_name,
                    "timestamp": datetime.utcnow().isoformat(),
                    "payload": payload,
                }
            )
        await self._dispatch(event_name, payload)

    async def _dispatch(self, event_name: str, payload: Dict[str, Any]) -> None:
        """Send events to local handlers plus plugin hooks."""
        handlers = self._subscribers.get(event_name, [])
        self._notify_plugins(event_name, payload)
        if not handlers:
            return
        tasks = [asyncio.create_task(handler(payload)) for handler in handlers]
        await asyncio.gather(*tasks)

    def publish(self, event_name: str, payload: Dict[str, Any]) -> None:
        """Fire-and-forget publish helper for synchronous callers."""
        asyncio.create_task(self.publish_async(event_name, payload))

    def register_plugin_hook(self, hook: PluginHook) -> None:
        """Allow plugins to observe every event."""
        if hook not in self._plugin_hooks:
            self._plugin_hooks.append(hook)

    def _notify_plugins(self, event_name: str, payload: Dict[str, Any]) -> None:
        for hook in list(self._plugin_hooks):
            try:
                result = hook(event_name, payload)
                if inspect.isawaitable(result):
                    asyncio.create_task(result)  # run hook asynchronously
            except Exception:
                continue

    def get_log(self) -> List[Dict[str, Any]]:
        """Return a copy of the rolling log."""
        return list(self._log)


event_bus = EventBus()

