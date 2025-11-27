"""
Asynchronous EventBus with basic history tracking.
"""

import asyncio
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


event_bus = EventBus()
