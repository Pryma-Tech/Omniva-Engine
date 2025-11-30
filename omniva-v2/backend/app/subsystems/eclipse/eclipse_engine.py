"""Crisis mode orchestration for Omniva Eclipse."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/eclipse/eclipse_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/eclipse/eclipse_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/eclipse/eclipse_engine with cognitive telemetry.


from __future__ import annotations

from typing import Dict, List, Set


class EclipseEngine:
    """
    Orchestrates crisis detection, recovery actions, and quarantining.
    """

    def __init__(self, registry, detector, recovery) -> None:
        self.registry = registry
        self.detector = detector
        self.recovery = recovery
        self.quarantined_nodes: Set[str] = set()

    def evaluate(self) -> Dict[str, List[str]]:
        crisis = self.detector.scan()
        return {"crisis_flags": crisis}

    def quarantine_node(self, node_id: str) -> Dict[str, object]:
        self.quarantined_nodes.add(node_id)
        return {"status": "node_quarantined", "node": node_id}

    def resolve(self) -> Dict[str, object]:
        crisis = self.detector.scan()
        if not crisis:
            return {"action": "none", "detail": "system_ok"}
        if len(crisis) <= 2:
            return {"action": "soft_rebuild", "detail": self.recovery.soft_rebuild()}
        if len(crisis) <= 5:
            return {"action": "subsystem_reset", "detail": self.recovery.subsystem_reset()}
        return {"action": "full_reboot", "detail": self.recovery.full_reboot()}

    def eclipse_snapshot(self) -> Dict[str, object]:
        return {
            "crisis": self.detector.scan(),
            "quarantined_nodes": list(self.quarantined_nodes),
            "reboot_log": self.recovery.get_logs(),
            "epoch": self.registry.archive.current_epoch,
        }
