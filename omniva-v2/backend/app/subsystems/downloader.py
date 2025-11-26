"""Downloader subsystem for Omniva Engine v2 (placeholder)."""

from app.core.registry import registry


class DownloaderSubsystem:
    """Placeholder downloader engine."""

    name = "downloader"

    def initialize(self) -> dict:
        return {"status": "downloader subsystem initialized (placeholder)"}

    def status(self) -> dict:
        return {"name": self.name, "status": "ok (placeholder)"}


registry.register_subsystem("downloader", DownloaderSubsystem())
