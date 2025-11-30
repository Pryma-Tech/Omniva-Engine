"""Safe plugin loader for Omniva Forge."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/forge/plugin_loader.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/forge/plugin_loader with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/forge/plugin_loader with cognitive telemetry.


from __future__ import annotations

import importlib.util
import os
from types import ModuleType

from app.forge.plugin_manifest import PluginManifest


class PluginLoader:
    """
    Loads plugin modules based on manifest.json definitions.
    """

    def load_module(self, plugin_dir: str, manifest: PluginManifest) -> ModuleType:
        path = os.path.join(plugin_dir, manifest.entrypoint)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Entrypoint '{manifest.entrypoint}' not found for plugin {manifest.name}")

        spec = importlib.util.spec_from_file_location(manifest.name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to load plugin module for {manifest.name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[union-attr]
        return module
