"""Master emotional resonance orchestrator for Omniva Chorus."""

from __future__ import annotations

from typing import Dict


class ChorusEngine:
    """Provides emotional field and modulation snapshots."""

    def __init__(self, registry, resonance, harmonics) -> None:
        self.registry = registry
        self.resonance = resonance
        self.harmonics = harmonics

    def emotional_field(self) -> Dict[str, float]:
        return self.resonance.compute_field()

    def modulation(self) -> Dict[str, float]:
        field = self.emotional_field()
        return self.harmonics.generate_modulation(field)

    def chorus_snapshot(self) -> Dict[str, object]:
        field = self.emotional_field()
        return {"field": field, "modulation": self.harmonics.generate_modulation(field)}
