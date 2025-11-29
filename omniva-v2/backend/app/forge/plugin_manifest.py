"""Plugin manifest loading utilities."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/forge/plugin_manifest.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/forge/plugin_manifest with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/forge/plugin_manifest with cognitive telemetry.


from __future__ import annotations

import json
from pathlib import Path
from typing import List

from pydantic import BaseModel


class PluginManifest(BaseModel):
    """Structured metadata describing a plugin."""

    name: str
    version: str
    description: str
    author: str
    entrypoint: str
    routes: List[str] = []
    commands: List[str] = []
    events: List[str] = []


def load_manifest(path: str | Path) -> PluginManifest:
    with open(path, "r", encoding="utf-8") as manifest_file:
        data = json.load(manifest_file)
    return PluginManifest(**data)
