"""Emotional modulation generator for Omniva Chorus."""

from __future__ import annotations

from typing import Dict


class HarmonicsEngine:
    """Converts emotional field into modulation signals."""

    def generate_modulation(self, field: Dict[str, float]) -> Dict[str, float]:
        tension = field.get("tension", 0.0)
        excitement = field.get("excitement", 0.0)
        instability = field.get("instability", 0.0)
        calm = field.get("calm", 0.0)
        modulation = {
            "risk_mod": min(1.0, excitement * 0.5 + tension * 0.3),
            "explore_mod": min(1.0, excitement * 0.7 + instability * 0.2),
            "focus_mod": max(0.0, calm * 0.7 - instability * 0.3),
            "planning_depth_mod": max(0.1, 1 - instability),
        }
        return {k: round(v, 4) for k, v in modulation.items()}
