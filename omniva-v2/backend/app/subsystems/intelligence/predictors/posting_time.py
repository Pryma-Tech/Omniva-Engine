"""
Posting time predictor with historical statistics.
"""

from datetime import datetime

from app.subsystems.intelligence.posting_stats_store import PostingStatsStore


class PostingTimePredictor:
    """Recommend posting slots based on project history."""

    def __init__(self) -> None:
        self.store = PostingStatsStore()

    def record_post(self, project_id: int, dt: datetime | None = None) -> None:
        if dt is None:
            dt = datetime.utcnow()
        self.store.record_post(project_id, dt)

    def predict_best_time(self, project_id: int) -> dict:
        best = self.store.best_slot(project_id)
        if not best:
            return {
                "project_id": project_id,
                "recommended_hour": 18,
                "recommended_weekday": 3,
                "source": "default",
            }
        return {
            "project_id": project_id,
            "recommended_hour": best["hour"],
            "recommended_weekday": best["weekday"],
            "uploads": best["uploads"],
            "score": best["score"],
            "source": "history",
        }
