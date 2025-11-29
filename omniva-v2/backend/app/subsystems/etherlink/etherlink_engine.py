"""Core distributed coordination logic for Omniva Etherlink."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/etherlink/etherlink_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/etherlink/etherlink_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/etherlink/etherlink_engine with cognitive telemetry.


from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional


class EtherlinkEngine:
    """
    Controls:
      - Node registration
      - Heartbeats
      - Event syncing
      - State replication
      - Distributed task routing
    """

    def __init__(self, registry, node_registry, sync_protocol) -> None:
        self.registry = registry
        self.node_registry = node_registry
        self.sync_protocol = sync_protocol

    def register_node(self, node_id: str, url: str, roles: List[str]) -> Dict[str, Any]:
        return self.node_registry.register(node_id, url, roles)

    def heartbeat(self, node_id: str) -> Dict[str, Any]:
        self.node_registry.update_heartbeat(node_id)
        return {"ok": True}

    async def emit_event(self, topic: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends event to all remote nodes.
        """
        await self.sync_protocol.broadcast_event(topic, payload)
        return {"ok": True}

    async def fetch_remote_state(self, node_id: str) -> Optional[Dict[str, Any]]:
        node = self.node_registry.get(node_id)
        if not node:
            return None
        return await self.sync_protocol.pull_state(str(node["url"]))

    def _project_manager(self):
        return (
            self.registry.get_subsystem("project_manager")
            or self.registry.get_subsystem("projects")
            or getattr(self.registry, "projects", None)
        )

    def local_state_snapshot(self) -> Dict[str, Any]:
        """
        Returns a lightweight system snapshot for syncing.
        """
        identity = self.registry.selfmodel.get_identity()
        epoch = self.registry.archive.current_epoch
        projects = self._project_manager()
        project_ids = projects.get_all_project_ids() if projects and hasattr(projects, "get_all_project_ids") else []
        return {
            "identity": identity,
            "epoch": epoch,
            "project_count": len(project_ids),
            "nodes": self.node_registry.list(),
            "timestamp": datetime.utcnow().isoformat(),
        }
