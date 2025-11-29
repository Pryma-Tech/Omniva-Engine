"""Archetypal governance controller for Omniva Pantheon."""

from __future__ import annotations

from typing import Dict


class PantheonEngine:
    """Provides consensus vectors and weight adjustments."""

    def __init__(self, registry, council) -> None:
        self.registry = registry
        self.council = council

    def compute_consensus(self, context=None) -> Dict[str, float]:
        return self.council.consensus(context or {})

    def adjust_weight(self, name: str, weight: float) -> Dict[str, Dict[str, float]]:
        self.council.set_weight(name, weight)
        return {"weights": self.council.weights}

    def pantheon_snapshot(self) -> Dict[str, object]:
        return {"weights": self.council.weights, "consensus": self.compute_consensus()}
