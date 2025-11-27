"""Keyword-based clip ranking (placeholder)."""


class KeywordRanker:
    """Score clip candidates based on keyword heuristics."""

    def rank(self, project_id: int, clips: list) -> list:
        # TODO: implement topic/keyword scoring
        return [{"clip": clip, "score": 0.5} for clip in clips]
