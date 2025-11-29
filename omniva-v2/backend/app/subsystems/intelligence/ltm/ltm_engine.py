"""Long-Term Memory Engine implementation."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from app.core.registry import registry
from .ltm_store import LTMStore


class LongTermMemoryEngine:
    """Archive intelligence state, detect drift, and surface memory health."""

    def __init__(self, store: LTMStore) -> None:
        self.store = store

    # ---------------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------------
    def _intel(self):
        intel = registry.get_subsystem("intelligence")
        if intel is None:
            raise RuntimeError("Intelligence subsystem is not registered")
        return intel

    def _keyword_snapshot(self, project_id: int) -> Dict[str, Any]:
        intel = self._intel()
        trends = intel.keyword_ranker.store.get_trends(project_id)
        sorted_trends = sorted(
            trends.items(), key=lambda entry: entry[1].get("count", 0), reverse=True
        )
        top_items = [
            {"keyword": keyword, "count": meta.get("count", 0)}
            for keyword, meta in sorted_trends[:5]
        ]
        total = sum(meta.get("count", 0) for meta in trends.values())
        return {"top": top_items, "total": total, "unique": len(trends)}

    def _audio_snapshot(self, project_id: int) -> Dict[str, Any]:
        intel = self._intel()
        tracks = intel.audio_trends.store.get_trending(project_id)
        sorted_tracks = sorted(
            tracks.items(), key=lambda entry: entry[1].get("count", 0), reverse=True
        )
        top_tracks = [
            {"audio_id": audio_id, "count": meta.get("count", 0)}
            for audio_id, meta in sorted_tracks[:5]
        ]
        total = sum(meta.get("count", 0) for meta in tracks.values())
        return {"top": top_tracks, "total": total, "unique": len(tracks)}

    def _semantic_snapshot(self, project_id: int) -> Dict[str, Any]:
        intel = self._intel()
        cache = intel.semantic_ranker.store.load(project_id)
        vectors = list(cache.get("cache", {}).values())
        dims = len(vectors[0]) if vectors else 0
        magnitudes = [sum(abs(val) for val in vec) for vec in vectors]
        avg_magnitude = round(sum(magnitudes) / len(magnitudes), 4) if magnitudes else 0.0
        return {
            "total_embeddings": len(vectors),
            "dims": dims,
            "avg_magnitude": avg_magnitude,
        }

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def snapshot(self, project_id: int) -> Dict[str, Any]:
        """Persist a snapshot of the current intelligence state."""

        intel = self._intel()
        snapshot = {
            "time": datetime.utcnow().isoformat(),
            "weights": intel.prioritizer.get_weights(),
            "keyword_stats": self._keyword_snapshot(project_id),
            "semantic_stats": self._semantic_snapshot(project_id),
            "audio_stats": self._audio_snapshot(project_id),
        }
        self.store.save_snapshot(project_id, snapshot)
        return snapshot

    def detect_drift(self, project_id: int) -> Dict[str, Any]:
        """Compare the latest two snapshots and record drift data."""

        data = self.store.load(project_id)
        snapshots = data.get("snapshots", [])
        if len(snapshots) < 2:
            record = {
                "time": datetime.utcnow().isoformat(),
                "drift_detected": False,
                "reason": "insufficient_snapshots",
                "delta": {},
            }
            self.store.record_drift(project_id, record)
            return record

        old = snapshots[-2]
        new = snapshots[-1]
        weight_delta = self._delta_map(new.get("weights", {}), old.get("weights", {}))
        keyword_delta = new["keyword_stats"].get("total", 0) - old["keyword_stats"].get("total", 0)
        audio_delta = new["audio_stats"].get("total", 0) - old["audio_stats"].get("total", 0)
        embedding_delta = (
            new["semantic_stats"].get("total_embeddings", 0)
            - old["semantic_stats"].get("total_embeddings", 0)
        )

        tolerance = intel.personality.drift_tolerance(project_id)
        drift_detected = self._drift_flag(
            weight_delta, keyword_delta, audio_delta, embedding_delta, tolerance
        )

        record = {
            "time": datetime.utcnow().isoformat(),
            "drift_detected": drift_detected,
            "delta": {
                "weights": weight_delta,
                "keywords": keyword_delta,
                "audio": audio_delta,
                "semantic": embedding_delta,
            },
        }
        self.store.record_drift(project_id, record)
        return record

    def consolidate(self, project_id: int) -> Dict[str, Any]:
        """Merge histories from optimizer/self-eval/decisions into a single summary."""

        intel = self._intel()
        self_eval = getattr(intel, "self_eval", None)
        self_eval_history = self_eval.get_history(project_id) if hasattr(self_eval, "get_history") else {}
        optimizer_history = intel.optimizer.get_history(project_id)
        decisions = self._load_decision_history(intel, project_id)

        self_eval_events = len(self_eval_history.get("history", [])) if isinstance(self_eval_history, dict) else 0
        optimizer_rounds = len(optimizer_history.get("runs", [])) if isinstance(optimizer_history, dict) else 0
        decision_events = len(decisions)

        consolidated = {
            "last_updated": datetime.utcnow().isoformat(),
            "totals": {
                "self_eval_events": self_eval_events,
                "optimizer_rounds": optimizer_rounds,
                "decision_events": decision_events,
            },
            "final_weights": optimizer_history.get("final_weights") if isinstance(optimizer_history, dict) else None,
            "notes": self._generate_notes(self_eval_events, optimizer_rounds, decision_events),
        }

        self.store.update_consolidated(project_id, consolidated)
        return consolidated

    def memory_report(self, project_id: int) -> Dict[str, Any]:
        """Return the aggregated long-term memory health report."""

        data = self.store.load(project_id)
        health = self._health_status(data)
        return {
            "project_id": project_id,
            "snapshots": data.get("snapshots", []),
            "drift_log": data.get("drift_log", []),
            "consolidated": data.get("consolidated", {}),
            "health": health,
        }

    # ------------------------------------------------------------------
    # Internal utilities
    # ------------------------------------------------------------------
    @staticmethod
    def _delta_map(new: Dict[str, float], old: Dict[str, float]) -> Dict[str, float]:
        keys = set(new) | set(old)
        return {key: round(new.get(key, 0.0) - old.get(key, 0.0), 4) for key in keys}

    @staticmethod
    def _drift_flag(
        weight_delta: Dict[str, float],
        keyword_delta: float,
        audio_delta: float,
        embedding_delta: float,
        tolerance: float,
    ) -> bool:
        if any(abs(value) > tolerance for value in weight_delta.values()):
            return True
        keyword_limit = 50 * max(0.2, min(2.0, tolerance / 0.05))
        if abs(keyword_delta) > keyword_limit:
            return True
        audio_limit = 30 * max(0.2, min(2.0, tolerance / 0.05))
        if abs(audio_delta) > audio_limit:
            return True
        embedding_limit = 25 * max(0.2, min(2.0, tolerance / 0.05))
        if abs(embedding_delta) > embedding_limit:
            return True
        return False

    @staticmethod
    def _generate_notes(self_eval_events: int, optimizer_rounds: int, decision_events: int) -> str:
        parts = []
        parts.append(f"self-eval events: {self_eval_events}")
        parts.append(f"optimizer rounds: {optimizer_rounds}")
        parts.append(f"decision events: {decision_events}")
        return "; ".join(parts)

    @staticmethod
    def _load_decision_history(intel, project_id: int) -> List[Dict[str, Any]]:
        decision_layer = getattr(intel, "decision_history", None)
        if callable(decision_layer):
            try:
                history = decision_layer(project_id)
                if isinstance(history, list):
                    return history
            except Exception:  # pragma: no cover - defensive guard
                return []
        if hasattr(decision_layer, "get_history"):
            try:
                entries = decision_layer.get_history(project_id)
                if isinstance(entries, list):
                    return entries
            except Exception:  # pragma: no cover
                return []
        return []

    @staticmethod
    def _health_status(data: Dict[str, Any]) -> Dict[str, Any]:
        drift_log = data.get("drift_log", [])
        latest_drift = drift_log[-1] if drift_log else None
        state = "stable"
        risk = "low"
        if latest_drift and latest_drift.get("drift_detected"):
            state = "drifting"
            risk = "medium"
        snapshot_count = len(data.get("snapshots", []))
        if snapshot_count == 0:
            state = "unknown"
            risk = "unknown"
        return {
            "state": state,
            "risk": risk,
            "total_snapshots": snapshot_count,
            "last_drift": latest_drift,
        }
