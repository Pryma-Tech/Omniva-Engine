"""Rule-based temporal anomaly detection for Omniva Paradox."""

from __future__ import annotations


class ParadoxRules:
    """
    Defines rule-based anomaly checks across:
      - Oracle forecasts
      - Astral futures
      - Infinity scaling
      - Emotional/drift stability
      - Epoch transitions
    """

    def drift_spike(self, curr: float, prev: float) -> bool:
        return abs(curr - prev) > 0.5

    def negative_trend(self, trend: float) -> bool:
        return trend < 0.0

    def infinity_mismatch(self, load_score: float, scale: int) -> bool:
        return load_score < 0.1 and scale > 5

    def astral_divergence(self, branches) -> bool:
        if not branches:
            return False
        for _, seq in branches.items():
            if len(seq) < 2:
                continue
            diffs = abs(seq[-1]["trend"] - seq[0]["trend"])
            if diffs > 0.7:
                return True
        return False
