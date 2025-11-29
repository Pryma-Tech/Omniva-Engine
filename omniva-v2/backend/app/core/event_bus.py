"""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/core/event_bus.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/core/event_bus with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/core/event_bus with cognitive telemetry.

Asynchronous EventBus with basic history tracking.
"""

import asyncio
import inspect
from collections import defaultdict
from datetime import datetime
from typing import Any, Awaitable, Callable, DefaultDict, Dict, List

AsyncHandler = Callable[[Dict[str, Any]], Awaitable[None]]


class EventBus:
    """Async pub/sub event bus with in-memory log."""

    def __init__(self) -> None:
        self.subscribers: DefaultDict[str, List[AsyncHandler]] = defaultdict(list)
        self.event_log: List[Dict[str, Any]] = []
        self.lock = asyncio.Lock()
        self.plugin_hooks: List[Callable[[str, Dict[str, Any]], Any]] = []

    def subscribe(self, event_name: str, callback: AsyncHandler) -> None:
        """Register an async handler for the event."""
        self.subscribers[event_name].append(callback)

    async def publish_async(self, event_name: str, data: Dict[str, Any]) -> None:
        """Dispatch an event to subscribers asynchronously."""
        async with self.lock:
            self.event_log.append(
                {
                    "event": event_name,
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": data,
                }
            )
        self._symbolic_observer(event_name, data)
        self._archive_observer(event_name, data)
        self._plugin_observer(event_name, data)
        self._stardust_observer(event_name, data)

        handlers = self.subscribers.get(event_name, [])
        tasks = [asyncio.create_task(handler(data)) for handler in handlers]
        if tasks:
            await asyncio.gather(*tasks)

    def publish(self, event_name: str, data: Dict[str, Any]) -> None:
        """Fire-and-forget wrapper for publish_async."""
        asyncio.create_task(self.publish_async(event_name, data))

    def get_log(self) -> List[Dict[str, Any]]:
        """Return a snapshot of the event log."""
        return list(self.event_log)

    def _symbolic_observer(self, event_name: str, data: Dict[str, Any]) -> None:
        """Forward events to the Soul Bind layer if available."""
        try:
            from app.core.registry import registry
        except Exception:
            return
        soul = getattr(registry, "soul", None) or registry.get_subsystem("soul")
        if not soul:
            return
        try:
            soul.interpret_event(event_name, data)
        except Exception:
            # Symbolic logging should never break the pipeline.
            pass

    def _archive_observer(self, event_name: str, data: Dict[str, Any]) -> None:
        try:
            from app.core.registry import registry
        except Exception:
            return
        archive = getattr(registry, "archive", None) or registry.get_subsystem("archive")
        if not archive:
            return
        try:
            archive.record(event_name, data)
            archive.update_epoch()
        except Exception:
            pass

    def register_plugin_hook(self, handler: Callable[[str, Dict[str, Any]], Any]) -> None:
        """Allow plugins to observe events in a safe manner."""
        if handler not in self.plugin_hooks:
            self.plugin_hooks.append(handler)

    def _plugin_observer(self, event_name: str, data: Dict[str, Any]) -> None:
        for handler in list(self.plugin_hooks):
            try:
                result = handler(event_name, data)
                if inspect.iscoroutine(result):
                    asyncio.create_task(result)
            except Exception:
                continue

    def _stardust_observer(self, event_name: str, data: Dict[str, Any]) -> None:
        try:
            from app.core.registry import registry
        except Exception:
            return
        stardust = getattr(registry, "stardust", None) or registry.get_subsystem("stardust")
        if not stardust:
            return
        try:
            stardust.attach_to_event(event_name, data)
        except Exception:
            pass


event_bus = EventBus()
