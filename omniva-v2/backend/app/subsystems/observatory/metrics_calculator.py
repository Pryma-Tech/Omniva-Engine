"""Helper utilities for computing observatory metrics."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/observatory/metrics_calculator.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/observatory/metrics_calculator with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/observatory/metrics_calculator with cognitive telemetry.


from __future__ import annotations

from statistics import mean
from typing import Dict, Iterable, List, Sequence


class MetricsCalculator:
    """
    Computes and formats various global system metrics.
    """

    def emotional_metrics(self, project_states: Sequence[Dict[str, float]]) -> Dict[str, float]:
        stresses = [state.get("stress", 0.0) for state in project_states]
        if not stresses:
            return {"avg_stress": 0.0, "max_stress": 0.0, "min_stress": 0.0}
        return {
            "avg_stress": mean(stresses),
            "max_stress": max(stresses),
            "min_stress": min(stresses),
        }

    def drift_metrics(self, project_states: Sequence[Dict[str, float]]) -> Dict[str, float]:
        drifts = [state.get("drift", 0.0) for state in project_states]
        if not drifts:
            return {"avg_drift": 0.0, "max_drift": 0.0, "min_drift": 0.0}
        return {
            "avg_drift": mean(drifts),
            "max_drift": max(drifts),
            "min_drift": min(drifts),
        }

    def trend_metrics(self, trend_scores: Iterable[float]) -> Dict[str, float]:
        scores = list(trend_scores)
        if not scores:
            return {"mean": 0.0, "max": 0.0, "min": 0.0}
        return {
            "mean": mean(scores),
            "max": max(scores),
            "min": min(scores),
        }

    def constellation_summary(self, similarity_pairs: Sequence[Dict]) -> Dict[str, Sequence[Dict]]:
        """
        Provide a condensed summary of cross-project similarity.
        """
        top = similarity_pairs[:5] if similarity_pairs else []
        return {"top_pairs": top}
