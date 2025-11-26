"""Placeholder Project model."""
# TODO: Replace with real database model using SQLAlchemy.


class Project:
    """Simple in-memory project structure."""

    def __init__(self, project_id: int, name: str, keywords: list, recency_days: int = 7):
        self.project_id = project_id
        self.name = name
        self.keywords = keywords
        self.recency_days = recency_days
        self.creators = []
        self.schedule = {"hour": 12, "minute": 0}
        self.active = False
