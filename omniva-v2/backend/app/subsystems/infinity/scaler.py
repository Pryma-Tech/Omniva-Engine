"""Elastic node scaling heuristics."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/infinity/scaler.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/infinity/scaler with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/infinity/scaler with cognitive telemetry.


from __future__ import annotations


class InfinityScaler:
    """
    Controls the scaling level for compute nodes.
    Uses:
      - load score
      - thresholds
      - cooldown timers
    """

    def __init__(self, registry) -> None:
        self.registry = registry
        self.current_scale = 1
        self.min_scale = 1
        self.max_scale = 10
        self.cooldown = 0

    def scale_decision(self, load_score: float) -> int:
        """
        Adjust scale based on load thresholds.
        """
        if self.cooldown > 0:
            self.cooldown -= 1
            return self.current_scale

        if load_score > 0.75 and self.current_scale < self.max_scale:
            self.current_scale += 1
            self.cooldown = 3
        elif load_score < 0.25 and self.current_scale > self.min_scale:
            self.current_scale -= 1
            self.cooldown = 3

        return self.current_scale
