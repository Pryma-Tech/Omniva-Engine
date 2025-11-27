"""Evergreen intelligence mode."""


class EvergreenMode:
    """Prioritize timeless content and consistency."""

    def __init__(self, engine) -> None:
        self.engine = engine

    def apply(self, project_id: int, context: dict) -> dict:
        return {"strategy": "evergreen", "weight": 0.4, "context": context}
