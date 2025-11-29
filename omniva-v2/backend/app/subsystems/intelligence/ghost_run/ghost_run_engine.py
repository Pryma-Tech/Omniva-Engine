"""Synthetic ghost-run simulator for the intelligence subsystem."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/intelligence/ghost_run/ghost_run_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/ghost_run/ghost_run_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/ghost_run/ghost_run_engine with cognitive telemetry.


from datetime import datetime
import random
from typing import Dict, List

from app.core.event_bus import event_bus
from app.core.registry import registry


class GhostRunEngine:
    """Performs offline-only autonomous simulations using cached/synthetic data."""

    def simulate_cycle(self, project_id: int, clips: List[dict], rounds: int = 1) -> Dict[str, object]:
        """Run one or more simulated scoring cycles without performing any real I/O."""

        intel = registry.get_subsystem("intelligence")
        if intel is None:
            raise RuntimeError("Intelligence subsystem is not registered")

        results: List[Dict[str, object]] = []

        for _ in range(max(1, rounds)):
            noise = lambda value: value * random.uniform(0.9, 1.1)  # noqa: E731

            semantic = intel.semantic_rank(project_id, clips)
            for entry in semantic:
                if "semantic_similarity" in entry:
                    entry["semantic_similarity"] = noise(entry["semantic_similarity"])

            keyword = intel.keyword_ranker.rank(project_id, clips)
            for entry in keyword:
                if "niche_score" in entry:
                    entry["niche_score"] = noise(entry["niche_score"])
                if "trend_score" in entry:
                    entry["trend_score"] = noise(entry["trend_score"])

            audio_scores = [
                {
                    "clip_id": clip.get("id"),
                    "audio_score": random.randint(0, 5),
                }
                for clip in clips
            ]

            prioritized = intel.prioritize_with_personality(project_id, semantic, keyword, audio_scores)
            recommendations = intel.recommend_clips(project_id, prioritized, limit=3)

            results.append(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "semantic": semantic,
                    "keyword": keyword,
                    "audio": audio_scores,
                    "prioritized": prioritized,
                    "recommendations": recommendations,
                }
            )

        payload = {
            "project_id": project_id,
            "rounds": max(1, rounds),
            "runs": results,
        }

        event_bus.publish("ghost_run_completed", payload)
        return payload
