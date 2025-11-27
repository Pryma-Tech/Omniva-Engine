"""Viral-first intelligence mode."""


class ViralFirstMode:
    """Bias toward high-engagement, trendy content."""

    def __init__(self, engine) -> None:
        self.engine = engine

    def apply(self, project_id: int, context: dict) -> dict:
        return {"strategy": "viral", "weight": 0.9, "context": context}
