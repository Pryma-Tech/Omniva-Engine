"""Adaptive timing controller for the autonomy kernel."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/autonomy/loop_controller.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/autonomy/loop_controller with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/autonomy/loop_controller with cognitive telemetry.


from __future__ import annotations

import random
from typing import Dict


class LoopController:
    """Compute loop delays based on cognitive and emotional state."""

    def __init__(self) -> None:
        self.state: Dict[int, Dict[str, float]] = {}

    def get_timing(self, project_id: int, emotion: Dict[str, float], cognition: Dict[str, float]) -> tuple[float, float]:
        """Return (micro_delay, macro_delay) seconds."""

        excitement = emotion.get("excitement", 0.5)
        stress = emotion.get("stress", 0.2)
        attention = cognition.get("attention", 1.0)

        base_micro = 2.0
        base_macro = 15.0

        micro = base_micro / max(0.5, attention + excitement)
        macro = base_macro / max(0.4, excitement + 0.5)
        macro *= 1 + stress * 0.4

        micro += random.uniform(-0.2, 0.2)
        macro += random.uniform(-1.0, 1.0)

        micro = max(0.5, micro)
        macro = max(5.0, macro)

        self.state[project_id] = {"micro": micro, "macro": macro}
        return micro, macro
