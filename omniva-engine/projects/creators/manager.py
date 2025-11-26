"""Manages creators assigned to projects."""
# TODO: Persist creator data in the database.

from utils.logger import logger

from .model import Creator


class CreatorManager:
    """In-memory creator registry."""

    def __init__(self):
        self.creators = {}
        self.project_creators = {}
        self.next_id = 1
        logger.info("CreatorManager initialized (placeholder).")

    def create_creator(self, platform: str, url: str) -> Creator:
        creator_id = self.next_id
        self.next_id += 1
        creator = Creator(creator_id, platform, url)
        self.creators[creator_id] = creator
        return creator

    def assign_to_project(self, project_id: int, creator_id: int) -> list:
        assigned = self.project_creators.setdefault(project_id, [])
        if creator_id not in assigned:
            assigned.append(creator_id)
        return assigned

    def list_for_project(self, project_id: int) -> list:
        ids = self.project_creators.get(project_id, [])
        return [self.creators[i] for i in ids if i in self.creators]

    def all_creators(self) -> list:
        return list(self.creators.values())
