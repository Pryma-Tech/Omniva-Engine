"""Identity rule set that keeps the global agent persona coherent."""

from __future__ import annotations

from typing import Dict


class IdentityRules:
    """
    Rule-based identity normalizer:
      - ensures emotional state + persona state are aligned
      - prevents contradictory identity traits
      - harmonizes agent temperament with global trends
      - stabilizes coherence over time
    """

    def normalize_temperament(self, temperament: str, avg_stress: float, global_emotion: float) -> str:
        """
        Align temperament with current stress and macro emotion levels.
        """
        if avg_stress > 0.7 and temperament == "playful":
            return "analytic"
        if avg_stress < 0.4 and global_emotion > 0.5:
            return "playful"
        return temperament

    def normalize_identity_traits(self, identity: Dict[str, float]) -> Dict[str, float]:
        """
        Generic trait coherence cleanup.
        """
        if identity.get("confidence", 0.5) < 0.3:
            identity["resilience"] = min(1.0, identity.get("resilience", 0.5) + 0.1)

        if identity.get("drift", 0.0) > 0.6:
            identity["exploration_bias"] = max(0.1, identity.get("exploration_bias", 0.5) - 0.2)

        return identity.copy()
