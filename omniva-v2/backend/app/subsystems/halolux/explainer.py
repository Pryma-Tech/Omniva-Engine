"""Decision explanation builder for HaloLux."""

from __future__ import annotations

from typing import Dict


class HaloExplainer:
    """Synthesizes explanations across subsystems."""

    def __init__(self, registry, lightfield) -> None:
        self.registry = registry
        self.lightfield = lightfield

    def explain_decision(self, project_id: int) -> Dict[str, object]:
        pantheon = self.registry.pantheon.compute_consensus()
        chorus = self.registry.chorus.modulation()
        oracle = self.registry.oracle.project_forecast(project_id)
        astral = self.registry.astral.alternate_futures(project_id)
        strategy = self.registry.strategy.recommend_for_project(project_id)
        return {
            "project_id": project_id,
            "pantheon_influence": pantheon,
            "emotional_modulation": chorus,
            "oracle_forecast": oracle,
            "astral_futures": astral,
            "strategy_output": strategy,
            "reasoning_chain": [
                "Pantheon consensus shapes behavioral intent.",
                "Chorus modulation adjusts risk and exploration.",
                "Oracle forecasts inform expected stress/drift.",
                "Astral futures explore parallel scenarios.",
                "Strategy synthesizes clips under these signals.",
                "Decision emerges from the weighted synthesis.",
            ],
        }

    def system_explain(self) -> Dict[str, object]:
        state = self.lightfield.capture_state()
        return {
            "lightfield": state,
            "meta": {"insight": "Cross-subsystem interpretability snapshot", "coverage": list(state.keys())},
        }
