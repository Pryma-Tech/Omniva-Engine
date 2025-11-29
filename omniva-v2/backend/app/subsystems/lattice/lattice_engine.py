"""Master semantic fabric controller for Omniva Lattice."""

from __future__ import annotations

from typing import Dict, List


class LatticeEngine:
    """
    Orchestrates node creation and multi-context routes across subsystems.
    """

    def __init__(self, registry, fabric, linker) -> None:
        self.registry = registry
        self.fabric = fabric
        self.linker = linker

    def update_project(self, project_id: int) -> Dict[str, str]:
        oracle_id = self.linker.link_project_forecast(project_id)
        astral_id = self.linker.link_astral_futures(project_id, oracle_id)
        infinity_id = self.linker.link_infinity_state(astral_id)
        paradox_id = self.linker.link_paradox(infinity_id)
        return {
            "oracle": oracle_id,
            "astral": astral_id,
            "infinity": infinity_id,
            "paradox": paradox_id,
        }

    def context_trace(self, node_id: str) -> List[str]:
        return self.fabric.multi_hop(node_id, depth=4)

    def lattice_snapshot(self) -> Dict[str, object]:
        return {"nodes": self.fabric.nodes, "edges": self.fabric.edges}
