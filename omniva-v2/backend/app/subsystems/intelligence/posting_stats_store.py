"""
Persistent store for posting-time statistics.
"""

import json
import os
from datetime import datetime
from typing import Any, Dict


class PostingStatsStore:
    """Maintain per-project posting slots and scores."""

    def __init__(self) -> None:
        self.base = os.path.join("storage", "intelligence", "posting_stats")
        os.makedirs(self.base, exist_ok=True)

    def _path(self, project_id: int) -> str:
        return os.path.join(self.base, f"{project_id}.json")

    def load(self, project_id: int) -> Dict[str, Any]:
        path = self._path(project_id)
        if not os.path.exists(path):
            return {
                "project_id": project_id,
                "timezone": "UTC",
                "slots": {},
            }
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def save(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        path = self._path(project_id)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
        return data

    def record_post(self, project_id: int, dt: datetime) -> None:
        payload = self.load(project_id)
        weekday = dt.weekday()
        hour = dt.hour
        key = f"{weekday}-{hour}"
        if key not in payload["slots"]:
            payload["slots"][key] = {"uploads": 0, "score": 0.0}
        slot = payload["slots"][key]
        slot["uploads"] += 1
        slot["score"] += 1.0
        self.save(project_id, payload)

    def best_slot(self, project_id: int) -> Dict[str, Any] | None:
        payload = self.load(project_id)
        slots = payload.get("slots", {})
        if not slots:
            return None
        best_key = None
        best_val = None
        for key, value in slots.items():
            if best_val is None or value["score"] > best_val["score"]:
                best_key = key
                best_val = value
        if not best_key or not best_val:
            return None
        weekday, hour = map(int, best_key.split("-"))
        return {
            "weekday": weekday,
            "hour": hour,
            "uploads": best_val["uploads"],
            "score": best_val["score"],
        }
