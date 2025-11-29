"""Core plugin management engine for Omniva Forge."""

from __future__ import annotations

import os
from types import ModuleType
from typing import Dict, List, cast

from fastapi import APIRouter

from app.forge.plugin_manifest import PluginManifest, load_manifest


class ForgeEngine:
    """
    Plugin system:
      - discover plugins
      - load manifests
      - load modules
      - run plugin init phases
      - register plugin routes, commands, and events
    """

    def __init__(self, registry) -> None:
        self.registry = registry
        self.plugins: Dict[str, Dict[str, object]] = {}
        self.plugin_dir = "plugins"
        self.loader = self.registry.forge_loader
        self.plugin_router = APIRouter(prefix="/plugins")

    def discover(self) -> List[str]:
        """
        Scan plugin directory.
        """
        found: List[str] = []
        if not os.path.exists(self.plugin_dir):
            return found

        for name in os.listdir(self.plugin_dir):
            plugin_path = os.path.join(self.plugin_dir, name)
            manifest_path = os.path.join(plugin_path, "manifest.json")
            if os.path.isdir(plugin_path) and os.path.exists(manifest_path):
                found.append(plugin_path)
        return found

    def load_plugin(self, plugin_path: str) -> Dict[str, object]:
        manifest_path = os.path.join(plugin_path, "manifest.json")
        manifest = load_manifest(manifest_path)
        module = self.loader.load_module(plugin_path, manifest)
        plugin = {
            "manifest": manifest,
            "module": module,
            "enabled": False,
            "path": plugin_path,
        }
        self.plugins[manifest.name] = plugin
        return plugin

    def enable_plugin(self, name: str) -> Dict[str, object]:
        if name not in self.plugins:
            return {"ok": False, "error": "plugin_not_found"}

        plugin = self.plugins[name]
        module = cast(ModuleType, plugin["module"])

        trust_level = self.registry.halo.get_plugin_trust().get(name, "sandboxed")
        if trust_level == "blocked":
            return {"ok": False, "error": "plugin_blocked_by_halo"}

        init_fn = getattr(module, "init", None)
        if callable(init_fn):
            init_fn(self.registry)

        register_commands = getattr(module, "register_commands", None)
        if callable(register_commands):
            register_commands(self.registry.sanctum_commands)

        register_routes = getattr(module, "register_routes", None)
        if callable(register_routes):
            register_routes(self.plugin_router)

        register_events = getattr(module, "register_events", None)
        if callable(register_events):
            self.registry.eventbus.register_plugin_hook(register_events)

        register_metrics = getattr(module, "register_metrics", None)
        if callable(register_metrics):
            register_metrics(getattr(self.registry, "metrics", None))

        plugin["enabled"] = True
        return {"ok": True, "message": f"plugin {name} enabled"}

    def disable_plugin(self, name: str) -> Dict[str, object]:
        if name not in self.plugins:
            return {"ok": False, "error": "plugin_not_found"}
        self.plugins[name]["enabled"] = False
        return {"ok": True, "message": f"plugin {name} disabled"}

    def list_plugins(self) -> Dict[str, Dict[str, object]]:
        summary: Dict[str, Dict[str, object]] = {}
        for name, plugin in self.plugins.items():
            manifest = cast(PluginManifest, plugin["manifest"])
            summary[name] = {
                "version": manifest.version,
                "path": plugin.get("path"),
                "enabled": plugin["enabled"],
            }
        return summary
