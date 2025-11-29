"""Collective governance council for Omniva Pantheon."""

from __future__ import annotations

from statistics import mean
from typing import Dict, List


class PantheonCouncil:
    """Manages archetype weights and consensus computation."""

    def __init__(self, archetypes: List) -> None:
        self.archetypes = archetypes
        self.weights: Dict[str, float] = {a.name: 1.0 for a in archetypes}

    def set_weight(self, name: str, weight: float) -> None:
        if name in self.weights:
            self.weights[name] = weight

    def consensus(self, context) -> Dict[str, float]:
        aggregated = {"risk": [], "explore": [], "stability": [], "creativity": []}
        for archetype in self.archetypes:
            vector = archetype.influence(context)
            weight = self.weights.get(archetype.name, 1.0)
            for key, value in vector.items():
                aggregated[key].append(value * weight)
        return {key: min(max(mean(values) if values else 0.0, 0.0), 1.0) for key, values in aggregated.items()}
