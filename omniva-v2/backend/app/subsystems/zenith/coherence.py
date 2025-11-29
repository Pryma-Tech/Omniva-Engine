"""System-wide coherence computation for Omniva Zenith."""

from __future__ import annotations

from typing import Dict


class ZenithCoherence:
    """Calculates global coherence proxies."""

    def __init__(self, registry) -> None:
        self.registry = registry

    def compute(self) -> float:
        horizon_score = self.registry.horizon.alignment_report().get("alignment_score", 0.5)
        chorus_field = self.registry.chorus.chorus_snapshot().get("field", {})
        pantheon_consensus = self.registry.pantheon.pantheon_snapshot().get("consensus", {})
        paradox_snapshot = self.registry.paradox.paradox_snapshot()
        infinity_snapshot = self.registry.infinity.infinity_snapshot()
        emotional_balance = 1 - chorus_field.get("instability", 0.0)
        archetype_balance = 1 - abs(pantheon_consensus.get("risk", 0.5) - pantheon_consensus.get("stability", 0.5))
        anomaly_penalty = sum(len(v) for v in paradox_snapshot.get("project_anomalies", {}).values()) * 0.05
        scaling_smoothness = 1 - abs(infinity_snapshot.get("load_score", 0.5) - 0.5)
        raw_score = (
            horizon_score * 0.3
            + emotional_balance * 0.2
            + archetype_balance * 0.2
            + scaling_smoothness * 0.2
            - anomaly_penalty
        )
        return round(max(0.0, min(1.0, raw_score)), 4)
