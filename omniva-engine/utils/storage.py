"""Storage subsystem for Omniva Engine."""
# TODO: Add file validation, cleanup, disk usage tracking.

import os

from utils.logger import logger

BASE_STORAGE = "storage"


class StorageManager:
    """Keep track of storage structure and path helpers."""

    def __init__(self, base_dir: str = BASE_STORAGE) -> None:
        self.base_dir = base_dir
        self.ensure_base_dirs()
        logger.info("StorageManager initialized (placeholder).")

    def ensure_base_dirs(self) -> None:
        """Ensure that the storage root and subfolders exist."""
        dirs = [
            os.path.join(self.base_dir, "raw"),
            os.path.join(self.base_dir, "clips"),
            os.path.join(self.base_dir, "uploads"),
            os.path.join(self.base_dir, "branding"),
            os.path.join(self.base_dir, "temp"),
            os.path.join(self.base_dir, "transcripts"),
        ]
        for directory in dirs:
            os.makedirs(directory, exist_ok=True)

    def project_dir(self, project_id: int) -> str:
        """Return path to project-specific directory."""
        path = os.path.join(self.base_dir, f"project_{project_id}")
        os.makedirs(path, exist_ok=True)
        return path

    def raw_video_path(self, project_id: int, filename: str) -> str:
        """Return path for raw video storage."""
        project_root = self.project_dir(project_id)
        folder = os.path.join(project_root, "raw")
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, filename)

    def clip_output_path(self, project_id: int, filename: str) -> str:
        """Return path for clip outputs."""
        project_root = self.project_dir(project_id)
        folder = os.path.join(project_root, "clips")
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, filename)

    def upload_ready_path(self, project_id: int, filename: str) -> str:
        """Return path for upload-ready clips."""
        project_root = self.project_dir(project_id)
        folder = os.path.join(project_root, "uploads")
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, filename)

    def temp_path(self, filename: str) -> str:
        """Return path in temp directory."""
        return os.path.join(self.base_dir, "temp", filename)

    def describe(self) -> dict:
        """Return a placeholder directory listing."""
        return {
            "base_dir": self.base_dir,
            "structure": [
                "raw/",
                "clips/",
                "uploads/",
                "branding/",
                "temp/",
                "transcripts/",
            ],
        }


storage_manager = StorageManager()
