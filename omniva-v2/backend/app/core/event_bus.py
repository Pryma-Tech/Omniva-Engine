"""Simple event bus (placeholder)."""
# TODO: Add async support and persistent topics.

from collections import defaultdict
from typing import Any, Callable, Dict, List

import logging

logger = logging.getLogger("omniva_v2")


class EventBus:
    """Publish/subscribe event hub."""

    def __init__(self):
        self._subscriptions: Dict[str, List[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, event: str, handler: Callable[[Any], None]) -> None:
        logger.info("Subscribed handler %s to event %s (placeholder)", handler.__name__, event)
        self._subscriptions[event].append(handler)

    def publish(self, event: str, payload: Any) -> None:
        logger.info("Publishing event %s (placeholder)", event)
        for handler in self._subscriptions.get(event, []):
            try:
                handler(payload)
            except Exception:  # pragma: no cover
                logger.exception("Handler error (placeholder)")


EVENT_BUS = EventBus()

def get_event_bus() -> EventBus:
    return EVENT_BUS

event_bus = EVENT_BUS
