"""Posting time predictor (placeholder)."""


class PostingTimePredictor:
    """Recommend posting windows per project."""

    def predict_best_time(self, project_id: int) -> dict:
        # TODO: replace with analytics-based predictor
        return {"project_id": project_id, "recommended_hour": 18, "confidence": 0.5}
