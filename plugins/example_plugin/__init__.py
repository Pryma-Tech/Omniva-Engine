"""Example plugin package helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from . import plugin as plugin_impl

MANIFEST_PATH = Path(__file__).with_name("manifest.json")

__all__ = ["load_manifest", "activate"]


def load_manifest() -> Dict[str, Any]:
    """Return the plugin manifest metadata."""
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def activate(registry, router=None, commands=None) -> Dict[str, Any]:
    """Initialize the plugin and optionally register routes/commands."""
    plugin_impl.init(registry)
    if commands is not None:
        plugin_impl.register_commands(commands)
    if router is not None:
        plugin_impl.register_routes(router)
    return load_manifest()
