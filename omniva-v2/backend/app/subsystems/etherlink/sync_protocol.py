"""Remote state and event synchronization helpers."""

from __future__ import annotations

from typing import Any, Dict, Optional

import httpx


class SyncProtocol:
    """
    Defines how nodes sync state and events.
    Uses token-based secured HTTP calls.
    """

    def __init__(self, registry, auth_token: str) -> None:
        self.registry = registry
        self.auth_token = auth_token

    async def send_event(self, node_url: str, topic: str, payload: Dict[str, Any]) -> bool:
        """
        Send a single event to a remote node.
        """
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    f"{node_url}/etherlink/event",
                    json={
                        "topic": topic,
                        "payload": payload,
                        "token": self.auth_token,
                    },
                    timeout=5,
                )
            return True
        except Exception:
            return False

    async def broadcast_event(self, topic: str, payload: Dict[str, Any]) -> None:
        """
        Broadcast event to all nodes.
        """
        for _, node in self.registry.node_registry.list().items():
            await self.send_event(str(node["url"]), topic, payload)

    async def pull_state(self, node_url: str) -> Optional[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{node_url}/etherlink/state",
                    params={"token": self.auth_token},
                    timeout=5,
                )
                response.raise_for_status()
                return response.json()
        except Exception:
            return None
