"""Creator model for scraping targets."""
# TODO: Add real validation and platform-specific metadata.


class Creator:
    """Simple data holder for creator metadata."""

    def __init__(self, creator_id: int, platform: str, url_or_username: str):
        self.creator_id = creator_id
        self.platform = platform
        self.url_or_username = url_or_username
        self.recency_days = 7
