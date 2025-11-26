"""Placeholder in-memory session store."""
# TODO: Replace with signed cookies or Redis session storage.

import uuid

from utils.logger import logger


class SessionManager:
    """Lightweight session tracking for dashboard authentication."""

    def __init__(self) -> None:
        self.sessions = {}
        logger.info("SessionManager initialized (placeholder).")

    def create_session(self, username: str) -> str:
        """Create a placeholder session with UUID token."""
        token = str(uuid.uuid4())
        self.sessions[token] = {"username": username}
        logger.info("Created placeholder session: %s", token)
        return token

    def get_session(self, token: str):
        """Return session data if token is known."""
        return self.sessions.get(token)

    def delete_session(self, token: str) -> bool:
        """Delete session if present."""
        if token in self.sessions:
            del self.sessions[token]
            logger.info("Deleted placeholder session: %s", token)
            return True
        return False


session_manager = SessionManager()
