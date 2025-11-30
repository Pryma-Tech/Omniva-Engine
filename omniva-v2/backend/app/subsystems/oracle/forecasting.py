"""Deterministic forecasting utilities for Omniva Oracle."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/oracle/forecasting.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/oracle/forecasting with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/oracle/forecasting with cognitive telemetry.


from __future__ import annotations

from statistics import mean
from typing import List


class ForecastingEngine:
    """
    Predicts future emotion/drift/trend values using:
      - weighted moving averages
      - linear extrapolation
      - bounded drift stabilization
    """

    def forecast_trend(self, history: List[float]) -> dict:
        if len(history) < 3:
            return {"expected": history[-1] if history else 0, "confidence": 0.2}

        last = history[-1]
        avg = mean(history[-3:])
        delta = last - history[-2]

        expected = last + (delta * 0.5) + ((avg - last) * 0.3)
        expected = max(0.0, min(1.0, expected))

        return {"expected": expected, "confidence": 0.6}

    def forecast_stress(self, history: List[float]) -> dict:
        if len(history) < 2:
            return {"expected": history[-1] if history else 0.3, "confidence": 0.2}

        return {
            "expected": max(0.0, min(1.0, mean(history[-3:]) * 0.95)),
            "confidence": 0.5,
        }

    def forecast_drift(self, history: List[float]) -> dict:
        if not history:
            return {"expected": 0.2, "confidence": 0.2}

        return {
            "expected": max(0.0, min(1.0, history[-1] * 0.9)),
            "confidence": 0.4,
        }
