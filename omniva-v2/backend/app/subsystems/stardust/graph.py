"""Attribution graph for Omniva Stardust."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/stardust/graph.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/stardust/graph with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/stardust/graph with cognitive telemetry.


from __future__ import annotations

from typing import Dict, List


class AttributionGraph:
    """
    Graph of all metadata packets and parent-child links.
    """

    def __init__(self) -> None:
        self.nodes: Dict[str, object] = {}
        self.children: Dict[str, List[str]] = {}
        self.parents: Dict[str, List[str]] = {}

    def add_packet(self, packet) -> None:
        self.nodes[packet.id] = packet
        for parent in packet.parents:
            self.children.setdefault(parent, []).append(packet.id)
            self.parents.setdefault(packet.id, []).append(parent)

    def lineage(self, packet_id: str) -> List[str]:
        visited = set()
        stack = [packet_id]
        trail: List[str] = []
        while stack:
            pid = stack.pop()
            if pid in visited:
                continue
            visited.add(pid)
            trail.append(pid)
            for parent in self.parents.get(pid, []):
                stack.append(parent)
        return trail

    def forward_influence(self, packet_id: str) -> List[str]:
        visited = set()
        stack = [packet_id]
        descendants: List[str] = []
        while stack:
            pid = stack.pop()
            if pid in visited:
                continue
            visited.add(pid)
            descendants.append(pid)
            for child in self.children.get(pid, []):
                stack.append(child)
        return descendants
