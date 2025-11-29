"""Master interpretability supervisor for Omniva HaloLux."""

from __future__ import annotations

from typing import Dict


class HaloLuxEngine:
    """Provides illumination and explanation reports."""

    def __init__(self, registry, lightfield, explainer) -> None:
        self.registry = registry
        self.lightfield = lightfield
        self.explainer = explainer

    def illuminate(self) -> Dict[str, object]:
        return self.lightfield.capture_state()

    def explain_decision(self, project_id: int) -> Dict[str, object]:
        return self.explainer.explain_decision(project_id)

    def halolux_snapshot(self) -> Dict[str, object]:
        return self.explainer.system_explain()
