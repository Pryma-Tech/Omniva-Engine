"""Temporal load analyzer for Omniva Infinity."""

from __future__ import annotations

from statistics import mean
from typing import List


class TemporalLoadBalancer:
    """
    Computes expected compute demand based on:
      - project activity
      - Oracle forecasts
      - Astral futures
      - scheduler queue depth
      - recent worker performance
    """

    def __init__(self, registry) -> None:
        self.registry = registry

    def compute_load_score(self) -> float:
        """
        Returns 0.0 - 1.0 indicating expected compute demand.
        """
        scheduler = self.registry.get_subsystem("scheduler") or getattr(self.registry, "scheduler", None)
        oracle = self.registry.get_subsystem("oracle") or getattr(self.registry, "oracle", None)

        projects = (
            self.registry.get_subsystem("project_manager")
            or self.registry.get_subsystem("projects")
            or getattr(self.registry, "projects", None)
        )
        project_ids: List[int] = projects.get_all_project_ids() if projects and hasattr(projects, "get_all_project_ids") else []
        trend_vals = []
        if oracle:
            for pid in project_ids:
                fc = oracle.project_forecast(pid)
                trend_vals.append(fc["trend"]["expected"])

        avg_trend = mean(trend_vals) if trend_vals else 0.3
        queue_len = scheduler.queue_length() if scheduler and hasattr(scheduler, "queue_length") else 0
        queue_factor = min(1.0, queue_len / 50.0)
        return max(0.0, min(1.0, (avg_trend * 0.6) + (queue_factor * 0.4)))
