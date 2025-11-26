"""StorageManager for Omniva (Placeholder)."""
# TODO: Wire into real filesystem operations.

from utils.logger import logger

from . import paths


class StorageManager:
    """Return directory metadata and placeholder stats."""

    def __init__(self):
        logger.info("StorageManager initialized (placeholder).")

    def ensure_project_dirs(self, project_id: int) -> dict:
        return {
            "project": paths.project_dir(project_id),
            "downloads": paths.downloads_dir(project_id),
            "edits": paths.edits_dir(project_id),
            "renders": paths.renders_dir(project_id),
            "temp": paths.temp_dir(project_id),
        }

    def get_dirs(self, project_id: int) -> dict:
        return self.ensure_project_dirs(project_id)

    def storage_stats(self) -> dict:
        return {
            "total_projects": "placeholder",
            "storage_used_mb": "placeholder",
            "storage_root": paths.BASE_DIR,
        }
