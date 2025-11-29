"""System-level vision controller for Omniva Horizon."""

from __future__ import annotations

from typing import Dict


class HorizonEngine:
    """Coordinates global vision and long-horizon goals."""

    def __init__(self, registry, goals, alignment) -> None:
        self.registry = registry
        self.goals = goals
        self.alignment = alignment

    def set_epoch_goal(self, goals: Dict[str, float]) -> Dict[str, object]:
        epoch = self.registry.archive.current_epoch
        return {"epoch": epoch, "goal": self.goals.set_epoch_goal(epoch, goals)}

    def get_epoch_goal(self) -> Dict[str, object] | None:
        epoch = self.registry.archive.current_epoch
        return self.goals.get_epoch_goal(epoch)

    def vision(self) -> Dict[str, float]:
        return self.goals.get_vision_vector()

    def alignment_report(self) -> Dict[str, object]:
        return self.alignment.measure_alignment()

    def adjust_vision(self, weights: Dict[str, float]) -> Dict[str, float]:
        return self.alignment.update_goal_bias(weights)

    def horizon_snapshot(self) -> Dict[str, object]:
        return {
            "epoch_goal": self.get_epoch_goal(),
            "vision": self.vision(),
            "alignment": self.alignment_report(),
        }
