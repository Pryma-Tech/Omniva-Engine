"""Track remote nodes participating in the Omniva swarm."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional


class NodeRegistry:
    """
    Tracks all remote nodes participating in the Omniva swarm.
    """

    def __init__(self) -> None:
        self.nodes: Dict[str, Dict[str, object]] = {}

    def register(self, node_id: str, url: str, roles: List[str]) -> Dict[str, object]:
        record = {
            "url": url,
            "roles": roles,
            "last_seen": datetime.utcnow().isoformat(),
            "status": "active",
        }
        self.nodes[node_id] = record
        return record

    def update_heartbeat(self, node_id: str) -> None:
        if node_id in self.nodes:
            self.nodes[node_id]["last_seen"] = datetime.utcnow().isoformat()
            self.nodes[node_id]["status"] = "active"

    def list(self) -> Dict[str, Dict[str, object]]:
        return self.nodes

    def get(self, node_id: str) -> Optional[Dict[str, object]]:
        return self.nodes.get(node_id)
