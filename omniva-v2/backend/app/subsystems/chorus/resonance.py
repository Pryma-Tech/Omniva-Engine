"""Collective emotional field synthesis for Omniva Chorus."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/chorus/resonance.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/chorus/resonance with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/chorus/resonance with cognitive telemetry.


from __future__ import annotations

from typing import Dict


class ResonanceField:
    """Produces the base emotional field from cross-system signals."""

    def __init__(self, registry) -> None:
        self.registry = registry

    def compute_field(self) -> Dict[str, float]:
        consensus = self.registry.pantheon.compute_consensus()
        oracle_summary = self.registry.oracle.system_summary()
        drift = oracle_summary.get("drift", 0.2)
        stress = oracle_summary.get("stress", 0.3)
        paradox = self.registry.paradox.paradox_snapshot()
        anomaly_count = sum(len(items) for items in paradox.get("project_anomalies", {}).values())
        alignment_score = self.registry.horizon.alignment_report().get("alignment_score", 0.5)
        field = {
            "tension": min(1.0, stress * 0.5 + drift * 0.3),
            "calm": max(0.0, alignment_score * 0.7),
            "excitement": min(1.0, consensus.get("explore", 0.0) * 0.6 + consensus.get("creativity", 0.0) * 0.4),
            "instability": min(1.0, anomaly_count * 0.1 + drift * 0.2),
        }
        return {k: round(v, 4) for k, v in field.items()}
