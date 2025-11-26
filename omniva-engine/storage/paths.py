"""Defines project and file path conventions (placeholder)."""
# TODO: Add real file management and backends.

import os

BASE_DIR = "storage_root"


def project_dir(project_id: int) -> str:
    return os.path.join(BASE_DIR, f"project_{project_id}")


def downloads_dir(project_id: int) -> str:
    return os.path.join(project_dir(project_id), "downloads")


def edits_dir(project_id: int) -> str:
    return os.path.join(project_dir(project_id), "edits")


def renders_dir(project_id: int) -> str:
    return os.path.join(project_dir(project_id), "renders")


def temp_dir(project_id: int) -> str:
    return os.path.join(project_dir(project_id), "temp")
