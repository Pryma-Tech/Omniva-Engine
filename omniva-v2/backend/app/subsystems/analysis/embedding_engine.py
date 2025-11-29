"""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/analysis/embedding_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/analysis/embedding_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/analysis/embedding_engine with cognitive telemetry.

Embedding-based scoring helpers for transcript segments.
"""

from typing import Iterable, List, Optional

import torch
from sentence_transformers import SentenceTransformer


class EmbeddingEngine:
    """Lightweight wrapper around SentenceTransformer for scoring."""

    def __init__(self) -> None:
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def score_segments(self, segments: List[dict], keywords: Optional[Iterable[str]] = None) -> List[float]:
        """
        Compute semantic scores for each transcript segment.
        """
        texts = [segment.get("text", "") for segment in segments]
        if not texts:
            return []

        embeddings = self.model.encode(texts, convert_to_tensor=True)
        scores = torch.norm(embeddings, dim=1).tolist()

        if keywords:
            for index, segment in enumerate(segments):
                lower_text = segment.get("text", "").lower()
                for keyword in keywords:
                    if keyword.lower() in lower_text:
                        scores[index] += 0.4

        max_score = max(scores) if scores else 1.0
        return [score / max_score if max_score else 0.0 for score in scores]
