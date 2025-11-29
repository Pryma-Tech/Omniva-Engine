"""Meta-optimizer that tunes prioritizer weights via ghost simulations."""

from datetime import datetime
import statistics
from typing import Dict, List

from app.core.registry import registry
from .opt_store import SelfOptStore


class MetaOptimizerEngine:
    """Runs multi-round self-optimization informed by Ghost-Run simulations."""

    def __init__(self) -> None:
        self.store = SelfOptStore()

    def run(
        self,
        project_id: int,
        clips: List[dict],
        rounds: int = 5,
        ghost_rounds: int = 5,
    ) -> Dict[str, object]:
        intel = registry.get_subsystem("intelligence")
        if intel is None:
            raise RuntimeError("Intelligence subsystem not registered")

        prioritizer = intel.prioritizer
        history: List[Dict[str, object]] = []

        for current_round in range(max(1, rounds)):
            ghost = intel.ghost_run(project_id, clips, rounds=max(1, ghost_rounds))

            all_scores: List[float] = []
            for sim in ghost.get("runs", []):
                for rec in sim.get("recommendations", []):
                    score = rec.get("final_score")
                    if score is None:
                        score = rec.get("priority")
                    if score is not None:
                        all_scores.append(float(score))

            avg_score = statistics.mean(all_scores) if all_scores else 0.0
            var_score = statistics.pvariance(all_scores) if len(all_scores) > 1 else 0.0

            weights = dict(prioritizer.get_weights() or {})
            if not weights:
                # Fallback defaults if prioritizer hasn't been configured.
                weights = {
                    "semantic": 0.35,
                    "keyword": 0.25,
                    "trending": 0.2,
                    "audio": 0.2,
                }

            semantic = weights.get("semantic", 0.0)
            if var_score > 0.02:
                semantic += 0.02
            else:
                semantic = max(0.0, semantic - 0.01)
            weights["semantic"] = semantic

            if avg_score < 0.5:
                weights["trending"] = weights.get("trending", 0.0) + 0.015
                weights["keyword"] = weights.get("keyword", 0.0) + 0.015
            else:
                weights["audio"] = weights.get("audio", 0.0) + 0.01

            total = sum(weights.values()) or 1.0
            normalized = {k: round(max(v, 0.0) / total, 4) for k, v in weights.items()}

            prioritizer.set_weights(normalized)

            record = {
                "round": current_round + 1,
                "timestamp": datetime.utcnow().isoformat(),
                "avg_score": avg_score,
                "variance": var_score,
                "weights": normalized,
            }

            history.append(record)
            self.store.record_run(project_id, record)

        final_weights = prioritizer.get_weights()
        self.store.set_final_weights(project_id, final_weights)

        return {
            "project_id": project_id,
            "rounds": history,
            "final_weights": final_weights,
        }

    def get_history(self, project_id: int) -> Dict[str, object]:
        return self.store.load(project_id)
