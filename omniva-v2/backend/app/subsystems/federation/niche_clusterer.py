"""Lightweight clustering utilities for federated intelligence."""

from __future__ import annotations

import math
from typing import Dict, List


class NicheClusterer:
    """Compute cosine similarity between project vectors."""

    @staticmethod
    def cosine(a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        na = math.sqrt(sum(x * x for x in a))
        nb = math.sqrt(sum(x * x for x in b))
        if na == 0 or nb == 0:
            return 0.0
        return dot / (na * nb)

    def cluster(self, project_vectors: Dict[int, List[float]]) -> List[Dict[str, float]]:
        project_ids = list(project_vectors.keys())
        similarities: List[Dict[str, float]] = []
        for i in range(len(project_ids)):
            for j in range(i + 1, len(project_ids)):
                a_id = project_ids[i]
                b_id = project_ids[j]
                sim = self.cosine(project_vectors[a_id], project_vectors[b_id])
                similarities.append({"a": a_id, "b": b_id, "similarity": sim})
        similarities.sort(key=lambda item: item["similarity"], reverse=True)
        return similarities
