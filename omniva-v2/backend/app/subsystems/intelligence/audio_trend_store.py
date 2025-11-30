"""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/intelligence/audio_trend_store.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/audio_trend_store with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/audio_trend_store with cognitive telemetry.

Persistent store for trending audio usage.
"""

import json
import os
from datetime import date
from typing import Any, Dict


class AudioTrendStore:
    """Track audio usage per project."""

    def __init__(self) -> None:
        self.base = os.path.join("storage", "intelligence", "audio_trends")
        os.makedirs(self.base, exist_ok=True)

    def _path(self, project_id: int) -> str:
        return os.path.join(self.base, f"{project_id}.json")

    def load(self, project_id: int) -> Dict[str, Any]:
        path = self._path(project_id)
        if not os.path.exists(path):
            return {
                "project_id": project_id,
                "tracks": {},
                "last_update": None,
            }
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def save(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        path = self._path(project_id)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
        return data

    def record_audio(self, project_id: int, audio_id: str, meta: Dict[str, Any] | None = None) -> Dict[str, Any]:
        data = self.load(project_id)
        today = str(date.today())
        entry = data["tracks"].setdefault(
            audio_id,
            {"count": 0, "last_seen": today, "meta": meta or {}},
        )
        entry["count"] += 1
        entry["last_seen"] = today
        if meta:
            entry["meta"] = meta
        data["last_update"] = today
        return self.save(project_id, data)

    def get_trending(self, project_id: int) -> Dict[str, Any]:
        return self.load(project_id)["tracks"]
