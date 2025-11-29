"""Recovery rituals and reboot orchestration for Omniva Eclipse."""

from __future__ import annotations

import time
from typing import Dict, List


class RecoveryEngine:
    """
    Performs progressive recovery phases.
    """

    def __init__(self, registry) -> None:
        self.registry = registry
        self.reboot_log: List[Dict[str, object]] = []

    def soft_rebuild(self) -> Dict[str, str]:
        self.registry.eventbus.publish("eclipse.soft_rebuild", {})
        self.registry.selfmodel.recompute_identity()
        return {"status": "soft_rebuild_complete"}

    def subsystem_reset(self) -> Dict[str, str]:
        self.registry.eventbus.publish("eclipse.subsystem_reset", {})
        scheduler = self.registry.get_subsystem("scheduler") or getattr(self.registry, "scheduler", None)
        if scheduler and hasattr(scheduler, "reset_queue"):
            scheduler.reset_queue()
        return {"status": "subsystem_reset_complete"}

    def full_reboot(self) -> Dict[str, object]:
        """
        Epoch +1, reset drift, re-evaluate Oracle, and mark reboot log.
        """
        epoch = self.registry.archive.current_epoch
        self.registry.archive.update_epoch()
        log_entry = {
            "previous_epoch": epoch,
            "new_epoch": self.registry.archive.current_epoch,
            "timestamp": time.time(),
        }
        self.reboot_log.append(log_entry)
        identity = self.registry.selfmodel.get_identity()
        identity["drift_strength"] = 0.1
        self.registry.eventbus.publish("eclipse.full_reboot", log_entry)
        return {"status": "full_reboot_complete", "log": log_entry}

    def get_logs(self) -> List[Dict[str, object]]:
        return self.reboot_log
