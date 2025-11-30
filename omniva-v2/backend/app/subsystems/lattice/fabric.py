"""Universal inter-system relation index for Omniva Lattice."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/lattice/fabric.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/lattice/fabric with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/lattice/fabric with cognitive telemetry.


from __future__ import annotations

from collections import defaultdict
from typing import Dict, List


class LatticeFabric:
    """
    Global relational map holding nodes and typed edges.
    """

    def __init__(self) -> None:
        self.nodes: Dict[str, Dict] = {}
        self.edges: Dict[str, List[Dict[str, str]]] = defaultdict(list)

    def register_node(self, node_id: str, meta: Dict) -> None:
        self.nodes[node_id] = meta

    def link(self, source_id: str, target_id: str, edge_type: str) -> None:
        self.edges[source_id].append({"target": target_id, "type": edge_type})

    def get_node(self, node_id: str) -> Dict | None:
        return self.nodes.get(node_id)

    def get_links(self, node_id: str) -> List[Dict[str, str]]:
        return self.edges.get(node_id, [])

    def multi_hop(self, start_id: str, depth: int = 3) -> List[str]:
        visited = set()
        frontier: List[tuple[str, int]] = [(start_id, 0)]
        results: List[str] = []
        while frontier:
            node_id, dist = frontier.pop(0)
            if dist > depth or node_id in visited:
                continue
            visited.add(node_id)
            results.append(node_id)
            for link in self.edges.get(node_id, []):
                frontier.append((link["target"], dist + 1))
        return results
