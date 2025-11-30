"""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/subsystems/intelligence/trending_store.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/trending_store with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/trending_store with cognitive telemetry.

Persistent store for trending keywords.
"""

import json
import os
from datetime import date
from typing import Dict, List


class TrendingKeywordStore:
    """Maintain heatmap data per project."""

    def __init__(self) -> None:
        self.base = os.path.join("storage", "intelligence", "trending_keywords")
        os.makedirs(self.base, exist_ok=True)

    def _path(self, project_id: int) -> str:
        return os.path.join(self.base, f"{project_id}.json")

    def load(self, project_id: int) -> Dict[str, any]:
        path = self._path(project_id)
        if not os.path.exists(path):
            return {
                "project_id": project_id,
                "keywords": {},
                "last_update": None,
            }
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def save(self, project_id: int, data: Dict[str, any]) -> Dict[str, any]:
        path = self._path(project_id)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
        return data

    def add_keywords(self, project_id: int, keywords: List[str]) -> Dict[str, any]:
        payload = self.load(project_id)
        today = str(date.today())
        for keyword in keywords:
            kw = keyword.lower().strip()
            if not kw:
                continue
            entry = payload["keywords"].setdefault(kw, {"count": 0, "last_seen": today})
            entry["count"] += 1
            entry["last_seen"] = today
        payload["last_update"] = today
        return self.save(project_id, payload)

    def get_trends(self, project_id: int) -> Dict[str, any]:
        return self.load(project_id)["keywords"]
