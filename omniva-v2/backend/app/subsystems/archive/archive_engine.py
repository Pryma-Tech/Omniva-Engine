"""Chronological archive for Omniva."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, List


class ArchiveEngine:
    """
    Complete chronological record of Omniva's internal evolution.
    Tracks:
      - events
      - timelines
      - epochs
      - transitions
      - milestone detection
    """

    def __init__(self, registry, epoch_detector) -> None:
        self.registry = registry
        self.epoch_detector = epoch_detector
        self.timeline: List[Dict[str, Any]] = []
        self.epochs: List[Dict[str, Any]] = []
        self.current_epoch = "genesis"
        self.last_epoch_check = datetime.utcnow()

    def record(self, subsystem: str, event: Dict[str, Any]) -> Dict[str, Any]:
        timestamp = datetime.utcnow().isoformat()

        entry = {
            "time": timestamp,
            "subsystem": subsystem,
            "event": event,
            "epoch": self.current_epoch,
        }

        self.timeline.append(entry)
        if len(self.timeline) > 1000:
            self.timeline = self.timeline[-1000:]
        return entry

    def update_epoch(self) -> str:
        now = datetime.utcnow()
        if now - self.last_epoch_check < timedelta(hours=1):
            return self.current_epoch

        intel = self.registry.get_subsystem("intelligence") or getattr(self.registry, "intelligence", None)
        projects = self.registry.get_subsystem("project_manager") or self.registry.get_subsystem("projects")
        if not intel or not projects:
            self.last_epoch_check = now
            return self.current_epoch

        stresses: List[float] = []
        drifts: List[float] = []

        for pid in projects.get_all_project_ids():
            emo = intel.emotion_model.get(pid)
            drift = intel.cognition.drift.get(pid)
            stresses.append(emo.get("stress", 0.3))
            drifts.append(drift.get("drift_strength", 0.0))

        history = [{"stress": s, "drift": d} for s, d in zip(stresses, drifts)]
        new_epoch = self.epoch_detector.detect_epoch(history)

        if new_epoch != self.current_epoch:
            self.epochs.append({"time": now.isoformat(), "from": self.current_epoch, "to": new_epoch})
            if len(self.epochs) > 100:
                self.epochs = self.epochs[-100:]
            self.current_epoch = new_epoch

        self.last_epoch_check = now
        return self.current_epoch

    def summary(self) -> Dict[str, Any]:
        return {
            "current_epoch": self.current_epoch,
            "epochs": self.epochs[-10:],
            "timeline_length": len(self.timeline),
            "recent_events": self.timeline[-20:],
        }
