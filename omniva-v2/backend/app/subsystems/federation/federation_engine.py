"""Federated intelligence aggregation and sharing."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/federation/federation_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/federation/federation_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/federation/federation_engine with cognitive telemetry.


from __future__ import annotations

from statistics import mean
from typing import Dict, List


class FederatedIntelligenceEngine:
    """Aggregate cross-project signals and share heuristics."""

    def __init__(self, registry, clusterer) -> None:
        self.registry = registry
        self.clusterer = clusterer
        self.semantic_centroids: Dict[int, List[float]] = {}
        self.trend_scores: Dict[int, float] = {}
        self.emotional_norms: Dict[int, float] = {}
        self.drift_profiles: Dict[int, float] = {}
        self.shared_heuristics: Dict = {}
        self.trend_history: Dict[int, List[float]] = {}

    def _compute_centroid(self, vectors: List[List[float]]) -> List[float]:
        if not vectors:
            return []
        dims = len(vectors[0])
        return [mean([vec[i] for vec in vectors]) for i in range(dims)]

    def update_project_stats(self, project_id: int) -> None:
        intel = self.registry.get_subsystem("intelligence")
        if intel is None:
            return
        cache = intel.semantic_ranker.store.load(project_id)
        vectors = list(cache.get("cache", {}).values())
        if vectors:
            self.semantic_centroids[project_id] = self._compute_centroid(vectors)
        projects = self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")
        clips = projects.get_project_clips(project_id) if projects and hasattr(projects, "get_project_clips") else []
        if clips:
            trend_score = mean([clip.get("trending", 0.0) for clip in clips])
            self.trend_scores[project_id] = trend_score
            history = self.trend_history.setdefault(project_id, [])
            history.append(trend_score)
            if len(history) > 50:
                self.trend_history[project_id] = history[-50:]
        emotion = intel.emotion_model.get(project_id)
        self.emotional_norms[project_id] = mean([
            emotion.get("excitement", 0.5),
            emotion.get("curiosity", 0.5),
            emotion.get("confidence", 0.5),
        ])
        drift = intel.cognition.drift.get(project_id).get("drift_strength", 0.0)
        self.drift_profiles[project_id] = drift

    def federated_update(self) -> Dict | None:
        if not self.semantic_centroids:
            return None
        clusters = self.clusterer.cluster(self.semantic_centroids)
        heuristic = {
            "global_trend": mean(self.trend_scores.values()) if self.trend_scores else 0,
            "global_emotion_baseline": mean(self.emotional_norms.values()) if self.emotional_norms else 0,
            "global_drift_baseline": mean(self.drift_profiles.values()) if self.drift_profiles else 0,
            "niche_similarity": clusters[:10],
        }
        self.shared_heuristics = heuristic
        return heuristic

    def share_to_project(self, project_id: int) -> Dict:
        return self.shared_heuristics or {}

    def get_trend_history(self, project_id: int) -> List[float]:
        return list(self.trend_history.get(project_id, []))
