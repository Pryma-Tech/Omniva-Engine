"""Metadata cosmos controller for Omniva Stardust."""

from __future__ import annotations

from typing import Dict, List, Optional

from app.subsystems.stardust.packet import MetadataPacket


class StardustEngine:
    """
    Coordinates metadata packet creation and provenance graph updates.
    """

    def __init__(self, registry, graph) -> None:
        self.registry = registry
        self.graph = graph

    def create_packet(self, ptype: str, payload: Dict, parents: Optional[List[str]] = None) -> Dict:
        packet = MetadataPacket(ptype, payload, parents)
        self.graph.add_packet(packet)
        return packet.to_dict()

    def attach_to_event(self, topic: str, payload: Dict) -> Dict:
        parents = payload.get("_meta_parents", [])
        meta_payload = {"topic": topic, "payload": payload}
        return self.create_packet("event", meta_payload, parents)

    def trace(self, packet_id: str) -> List[str]:
        return self.graph.lineage(packet_id)

    def influence(self, packet_id: str) -> List[str]:
        return self.graph.forward_influence(packet_id)

    def graph_snapshot(self) -> Dict[str, object]:
        return {
            "nodes": {nid: packet.to_dict() for nid, packet in self.graph.nodes.items()},
            "edges": self.graph.parents,
        }
