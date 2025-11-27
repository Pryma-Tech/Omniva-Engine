"""
Intelligence layer controller for Omniva Engine.
"""

from app.core.event_bus import event_bus
from app.core.registry import registry


class IntelligenceEngine:
    """Coordinates predictors and strategy modes."""

    name = "intelligence"

    def __init__(self) -> None:
        from .predictors.audio_trends import AudioTrendMatcher
        from .predictors.keyword_ranker import KeywordRanker
        from .predictors.posting_time import PostingTimePredictor
        from .modes.balanced import BalancedMode
        from .modes.evergreen import EvergreenMode
        from .modes.viral_first import ViralFirstMode

        self.posting_time = PostingTimePredictor()
        self.keyword_ranker = KeywordRanker()
        self.audio_trends = AudioTrendMatcher()

        self.modes = {
            "viral": ViralFirstMode(self),
            "evergreen": EvergreenMode(self),
            "balanced": BalancedMode(self),
        }
        self.current_mode = "balanced"

    def initialize(self) -> dict:
        return {"status": "intelligence engine initialized"}

    def set_mode(self, mode: str) -> dict:
        if mode in self.modes:
            self.current_mode = mode
            event_bus.publish("intelligence_mode_changed", {"mode": mode})
            return {"mode": mode}
        return {"error": "unknown mode", "available": list(self.modes.keys())}

    def choose_posting_time(self, project_id: int) -> dict:
        return self.posting_time.predict_best_time(project_id)

    def rank_clips(self, project_id: int, clip_candidates: list) -> list:
        return self.keyword_ranker.rank(project_id, clip_candidates)

    def match_audio(self, project_id: int, clip_meta: dict) -> dict:
        return self.audio_trends.match(project_id, clip_meta)

    def apply_mode(self, project_id: int, context: dict) -> dict:
        mode = self.modes[self.current_mode]
        return mode.apply(project_id, context)

    def get_posting_stats(self, project_id: int) -> dict:
        return self.posting_time.store.load(project_id)

    def status(self) -> dict:
        return {"mode": self.current_mode, "available_modes": list(self.modes.keys())}
