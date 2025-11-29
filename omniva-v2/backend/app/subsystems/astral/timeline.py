"""Timeline simulator for alternate Omniva futures."""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, List


class TimelineSimulator:
    """
    Generates alternate timelines by:
      - modifying input parameters
      - applying deterministic transition rules
      - evaluating future states
    """

    def __init__(self, registry, oracle) -> None:
        self.registry = registry
        self.oracle = oracle

    def step(self, state: Dict[str, float], params: Dict[str, float]) -> Dict[str, float]:
        """
        Deterministic transition model:
          - drift decays or amplifies
          - stress follows WMA
          - trend follows simple extrapolation
          - parameters (upload rate, clip selection bias, etc.) modify outcomes
        """
        drift = state["drift"]
        stress = state["stress"]
        trend = state["trend"]

        drift_next = max(0.0, min(1.0, drift * (0.9 - params.get("drift_mod", 0.0))))
        stress_next = max(0.0, min(1.0, stress * (0.92 - params.get("stress_mod", 0.0))))
        trend_next = max(0.0, min(1.0, trend + params.get("trend_push", 0.05)))

        return {
            "drift": drift_next,
            "stress": stress_next,
            "trend": trend_next,
        }

    def simulate(self, initial_state: Dict[str, float], params: Dict[str, float], horizon: int = 5) -> List[Dict[str, float]]:
        """
        Produce a sequence of future states.
        """
        timeline: List[Dict[str, float]] = []
        state = deepcopy(initial_state)

        for _ in range(horizon):
            state = self.step(state, params)
            timeline.append(deepcopy(state))

        return timeline
