"""Project-level governance policy definitions."""

from __future__ import annotations

from typing import Dict


class ProjectPolicy:
    """Manage per-project governance configuration."""

    DEFAULT_POLICY = {
        "allowed_platforms": ["youtube", "tiktok", "instagram"],
        "blocked_platforms": [],
        "allowed_creators": [],
        "blocked_creators": [],
        "max_daily_posts": 3,
        "min_minutes_between_posts": 30,
        "require_manual_review": False,
        "max_clip_reuse_per_week": 1,
    }

    def __init__(self) -> None:
        self.policies: Dict[int, Dict] = {}

    def get_policy(self, project_id: int) -> Dict:
        if project_id not in self.policies:
            self.policies[project_id] = dict(self.DEFAULT_POLICY)
        return self.policies[project_id]

    def update_policy(self, project_id: int, changes: Dict) -> Dict:
        policy = self.get_policy(project_id)
        for key, value in changes.items():
            if key in policy:
                policy[key] = value
        self.policies[project_id] = policy
        return policy
