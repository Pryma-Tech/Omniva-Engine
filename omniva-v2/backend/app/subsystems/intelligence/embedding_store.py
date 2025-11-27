"""
Persistent cache for text embeddings.
"""

import json
import os
from typing import Dict, List


class EmbeddingStore:
    """Store embeddings per project with a simple JSON cache."""

    def __init__(self) -> None:
        self.base = os.path.join("storage", "intelligence", "embeddings")
        os.makedirs(self.base, exist_ok=True)

    def _path(self, project_id: int) -> str:
        return os.path.join(self.base, f"{project_id}.json")

    def load(self, project_id: int) -> Dict[str, List[float]]:
        path = self._path(project_id)
        if not os.path.exists(path):
            return {"project_id": project_id, "cache": {}}
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def save(self, project_id: int, data: Dict[str, List[float]]) -> Dict[str, List[float]]:
        path = self._path(project_id)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
        return data

    def get(self, project_id: int, key: str) -> List[float] | None:
        cache = self.load(project_id)
        return cache["cache"].get(key)

    def set(self, project_id: int, key: str, embedding: List[float]) -> None:
        cache = self.load(project_id)
        cache["cache"][key] = embedding
        self.save(project_id, cache)
