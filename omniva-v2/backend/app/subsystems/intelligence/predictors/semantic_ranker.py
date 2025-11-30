"""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/intelligence/predictors/semantic_ranker.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/predictors/semantic_ranker with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/predictors/semantic_ranker with cognitive telemetry.

Semantic ranking predictor leveraging cached embeddings.
"""

import math
from typing import List

from app.core.registry import registry
from app.subsystems.intelligence.embedding_provider import EmbeddingProvider
from app.subsystems.intelligence.embedding_store import EmbeddingStore


def cosine(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(y * y for y in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


class SemanticRanker:
    """Rank clips based on cosine similarity to niche embeddings."""

    def __init__(self) -> None:
        self.store = EmbeddingStore()
        self.provider = EmbeddingProvider()

    def get_embedding(self, project_id: int, key: str, text: str) -> List[float]:
        cached = self.store.get(project_id, key)
        if cached is not None:
            return cached
        vec = self.provider.embed_text(text)
        self.store.set(project_id, key, vec)
        return vec

    def rank(self, project_id: int, clips: List[dict]) -> List[dict]:
        project_manager = registry.get_subsystem("project_manager")
        config = project_manager.get(project_id)
        keywords = config.get("keywords", [])

        keyword_vectors = [
            self.get_embedding(project_id, f"kw:{kw}", kw) for kw in keywords
        ]
        if keyword_vectors:
            niche_vec = [sum(col) / len(keyword_vectors) for col in zip(*keyword_vectors)]
        else:
            niche_vec = [0.0] * 64

        results: List[dict] = []
        for clip in clips:
            clip_id = clip.get("id")
            transcript = clip.get("transcript", "")
            clip_vec = self.get_embedding(project_id, f"clip:{clip_id}", transcript)
            similarity = cosine(clip_vec, niche_vec)
            results.append(
                {
                    "clip_id": clip_id,
                    "semantic_similarity": similarity,
                    "transcript_len": len(transcript),
                }
            )
        return sorted(results, key=lambda entry: entry["semantic_similarity"], reverse=True)
