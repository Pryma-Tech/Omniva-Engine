"""Balanced intelligence mode."""


class BalancedMode:
    """Blend viral and evergreen heuristics."""

    def __init__(self, engine) -> None:
        self.engine = engine

    def apply(self, project_id: int, context: dict) -> dict:
        return {"strategy": "balanced", "weight": 0.6, "context": context}
