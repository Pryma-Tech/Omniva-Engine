"""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/discovery/discovery_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/discovery/discovery_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/discovery/discovery_engine with cognitive telemetry.

Creator discovery engine for Omniva Engine v2.
"""

from typing import Dict, List

from app.core.registry import registry
from app.subsystems.discovery.seen_store import SeenPostsStore
from app.subsystems.discovery.scrapers.instagram import discover_instagram_posts
from app.subsystems.discovery.scrapers.tiktok import discover_tiktok_posts
from app.subsystems.discovery.scrapers.youtube import discover_youtube_posts


class DiscoveryEngine:
    """Discover new posts for all creators of a project."""

    name = "discovery"

    def __init__(self) -> None:
        self.seen = SeenPostsStore()

    def initialize(self) -> dict:
        return {"status": "discovery engine initialized"}

    def discover_for_creator(self, project_id: int, creator_url: str) -> List[str]:
        """Return unseen posts for a single creator."""
        if "tiktok.com" in creator_url:
            posts = discover_tiktok_posts(creator_url)
        elif "instagram.com" in creator_url:
            posts = discover_instagram_posts(creator_url)
        elif "youtube.com" in creator_url or "youtu.be" in creator_url:
            posts = discover_youtube_posts(creator_url)
        else:
            return []

        new_posts: List[str] = []
        for url in posts:
            if not self.seen.is_seen(project_id, url):
                new_posts.append(url)
                self.seen.add_seen(project_id, url)
        return new_posts

    def discover_for_project(self, project_id: int) -> List[str]:
        """Discover posts for every creator configured in the project."""
        manager = registry.get_subsystem("project_manager")
        project = manager.get(project_id)
        creators = project.get("creators", [])
        new_posts: List[str] = []
        for creator in creators:
            new_posts.extend(self.discover_for_creator(project_id, creator))
        return new_posts

    def discover_new_posts(self, project_id: int) -> List[str]:
        """Alias used by the autonomous engine."""
        return self.discover_for_project(project_id)

    def check_new_posts(self, project_id: int) -> List[str]:
        """
        Observability-friendly alias expected by the Nexus composer.
        """
        return self.discover_new_posts(project_id)

    def check_all_projects(self) -> Dict[int, List[str]]:
        """
        Run discovery across every registered project.
        """
        manager = registry.get_subsystem("project_manager")
        if not manager or not hasattr(manager, "get_all_project_ids"):
            return {}
        results: Dict[int, List[str]] = {}
        for project_id in manager.get_all_project_ids():
            results[project_id] = self.discover_for_project(project_id)
        return results

    def status(self) -> dict:
        return {"name": self.name, "status": "ok"}
