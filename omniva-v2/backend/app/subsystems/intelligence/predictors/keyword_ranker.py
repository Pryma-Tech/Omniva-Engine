"""
Keyword ranking engine leveraging trending store.
"""

from collections import Counter
from typing import List

from app.core.registry import registry
from app.subsystems.intelligence.trending_store import TrendingKeywordStore


class KeywordRanker:
    """Rank clips according to niche alignment and trending keywords."""

    def __init__(self) -> None:
        self.store = TrendingKeywordStore()

    def extract_keywords(self, transcript: str) -> List[str]:
        tokens = [token.strip(".,!?").lower() for token in transcript.split()]
        return [token for token in tokens if len(token) > 3]

    def rank(self, project_id: int, clips: List[dict]) -> List[dict]:
        manager = registry.get_subsystem("project_manager")
        project = manager.get(project_id)
        niche_keywords = [kw.lower() for kw in project.get("keywords", [])]
        trends = self.store.get_trends(project_id)

        results: List[dict] = []
        for clip in clips:
            transcript = clip.get("transcript", "")
            extracted = self.extract_keywords(transcript)
            self.store.add_keywords(project_id, extracted)
            freq = Counter(extracted)
            niche_score = sum(freq.get(kw, 0) for kw in niche_keywords)
            trend_score = sum(trends.get(kw, {}).get("count", 0) for kw in extracted)
            total = niche_score * 0.6 + trend_score * 0.4
            results.append(
                {
                    "clip_id": clip.get("id"),
                    "niche_score": niche_score,
                    "trend_score": trend_score,
                    "total_score": total,
                    "keywords": extracted,
                }
            )
        return sorted(results, key=lambda item: item["total_score"], reverse=True)
