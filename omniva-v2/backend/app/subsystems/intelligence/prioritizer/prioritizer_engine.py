"""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/intelligence/prioritizer/prioritizer_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/prioritizer/prioritizer_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/prioritizer/prioritizer_engine with cognitive telemetry.

Clip prioritization engine.
"""

from typing import Dict, List

from .weights import DEFAULT_WEIGHTS


class ClipPrioritizer:
    """Fuse different intelligence scores into a single priority ranking."""

    def __init__(self) -> None:
        self.weights = DEFAULT_WEIGHTS.copy()

    def fuse(
        self,
        project_id: int,
        semantic_scores: List[Dict[str, float]],
        keyword_scores: List[Dict[str, float]],
        audio_scores: List[Dict[str, float]],
    ) -> List[Dict[str, float]]:
        sem_lookup = {entry["clip_id"]: entry for entry in semantic_scores}
        kw_lookup = {entry["clip_id"]: entry for entry in keyword_scores}
        audio_lookup = {entry["clip_id"]: entry.get("audio_score", 0.0) for entry in audio_scores}

        results: List[Dict[str, float]] = []
        for clip_id, semantic in sem_lookup.items():
            niche = kw_lookup.get(clip_id, {}).get("niche_score", 0.0)
            trending = kw_lookup.get(clip_id, {}).get("trend_score", 0.0)
            audio = audio_lookup.get(clip_id, 0.0)

            normalized_sem = semantic["semantic_similarity"]
            normalized_kw = niche
            normalized_trending = trending / 10.0
            normalized_audio = audio / 5.0

            weight = self.weights
            priority = (
                normalized_sem * weight["semantic"]
                + normalized_kw * weight["keyword"]
                + normalized_trending * weight["trending"]
                + normalized_audio * weight["audio"]
            )

            results.append(
                {
                    "clip_id": clip_id,
                    "semantic": semantic["semantic_similarity"],
                    "keyword": niche,
                    "trending": trending,
                    "audio": audio,
                    "priority": round(priority, 6),
                }
            )
        results.sort(key=lambda entry: entry["priority"], reverse=True)
        return results

    def set_weights(self, new_weights: Dict[str, float]) -> Dict[str, float]:
        for key, value in new_weights.items():
            if key in self.weights:
                self.weights[key] = float(value)
        return self.weights

    def get_weights(self) -> Dict[str, float]:
        return self.weights
