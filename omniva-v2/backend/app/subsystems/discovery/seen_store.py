"""
Track previously discovered creator posts.
"""

import json
import os
from typing import Any, Dict


class SeenPostsStore:
    """Simple JSON store for seen post URLs per project."""

    def __init__(self) -> None:
        self.base = os.path.join("storage", "seen_posts")
        os.makedirs(self.base, exist_ok=True)

    def _path(self, project_id: int) -> str:
        return os.path.join(self.base, f"{project_id}.json")

    def load(self, project_id: int) -> Dict[str, Any]:
        path = self._path(project_id)
        if not os.path.exists(path):
            return {"project_id": project_id, "posts": []}
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def save(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        path = self._path(project_id)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2)
        return data

    def add_seen(self, project_id: int, post_url: str) -> None:
        data = self.load(project_id)
        if post_url not in data["posts"]:
            data["posts"].append(post_url)
            self.save(project_id, data)

    def is_seen(self, project_id: int, post_url: str) -> bool:
        return post_url in self.load(project_id)["posts"]
