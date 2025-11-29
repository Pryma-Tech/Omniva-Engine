"""Symbolic narrative engine for Omniva."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/soulbind/soulbind_engine.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/soulbind/soulbind_engine with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/soulbind/soulbind_engine with cognitive telemetry.


from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


class SoulBindEngine:
    """
    Maintains Omniva's symbolic identity:
      - lore entries
      - mythic interpretation of events
      - narrative continuity
      - symbolic tagging of system states
    """

    def __init__(self, registry, catalog) -> None:
        self.registry = registry
        self.catalog = catalog
        self.journal: List[Dict[str, Any]] = []

    def interpret_event(self, subsystem: str, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts a raw event into a symbolic, narrative-form entry.
        """
        lore = self.catalog.get_entry(subsystem)
        timestamp = datetime.utcnow().isoformat()

        entry = {
            "time": timestamp,
            "subsystem": subsystem,
            "symbolic": lore,
            "event": event,
        }

        self.journal.append(entry)
        if len(self.journal) > 200:
            self.journal = self.journal[-200:]

        self._store_in_selfmodel(entry)
        return entry

    def _store_in_selfmodel(self, entry: Dict[str, Any]) -> None:
        selfmodel = getattr(self.registry, "selfmodel", None) or self.registry.get_subsystem("selfmodel")
        if not selfmodel:
            return
        record = {
            "time": entry.get("time"),
            "subsystem": entry.get("subsystem"),
            "symbolic": entry.get("symbolic"),
        }
        recorder = getattr(selfmodel, "record_lore_entry", None)
        if callable(recorder):
            recorder(record)

    def get_journal(self) -> List[Dict[str, Any]]:
        return list(self.journal)

    def get_codex(self) -> Dict[str, Any]:
        """
        Returns a structured lore codex for UI display.
        """
        return {
            "identity_title": "The Codex of Omniva",
            "lore_entries": self.catalog.get_lore(),
            "journal": self.journal[-20:],
        }
