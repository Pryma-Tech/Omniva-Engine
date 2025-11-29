"""Simple working memory buffer for short-term cognitive state."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/intelligence/cognition/working_memory.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/cognition/working_memory with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/cognition/working_memory with cognitive telemetry.


from __future__ import annotations

from collections import deque
from typing import Any, Deque, Dict, List


class WorkingMemory:
    """Maintain the most recent cognitive events."""

    def __init__(self, limit: int = 20) -> None:
        self.limit = limit
        self.storage: Deque[Dict[str, Any]] = deque(maxlen=limit)

    def push(self, item: Dict[str, Any]) -> None:
        self.storage.append(item)

    def recent(self, count: int = 5) -> List[Dict[str, Any]]:
        if count <= 0:
            return []
        return list(self.storage)[-count:]

    def clear(self) -> bool:
        self.storage.clear()
        return True
