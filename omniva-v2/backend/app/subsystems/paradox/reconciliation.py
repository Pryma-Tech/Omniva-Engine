"""Anomaly reconciliation heuristics for Omniva Paradox."""

from __future__ import annotations


class ReconciliationEngine:
    """
    Applies correction heuristics when anomalies arise.
    """

    def reconcile_drift(self, curr: float, prev: float) -> float:
        if abs(curr - prev) > 0.5:
            return (curr + prev) / 2.0
        return curr

    def clamp_trend(self, value: float) -> float:
        return max(0.0, min(1.0, value))

    def fix_scale(self, load_score: float, scale: int) -> int:
        if load_score < 0.1 and scale > 5:
            return 2
        return scale

    def collapse_branch(self, branches):
        for scenario, seq in branches.items():
            for state in seq:
                state["trend"] = self.clamp_trend(state.get("trend", 0.0))
        return branches
