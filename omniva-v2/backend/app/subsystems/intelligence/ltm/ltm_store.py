"""Persistent storage helpers for the Long-Term Memory Engine."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/intelligence/ltm/ltm_store.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/ltm/ltm_store with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/ltm/ltm_store with cognitive telemetry.


import json
import os
from typing import Any, Dict


class LTMStore:
    """Persist memory snapshots, drift logs, and consolidated summaries per project."""

    def __init__(self) -> None:
        self.base = os.path.join("storage", "intelligence", "ltm")
        os.makedirs(self.base, exist_ok=True)

    def _path(self, project_id: int) -> str:
        return os.path.join(self.base, f"{project_id}.json")

    def _defaults(self, project_id: int) -> Dict[str, Any]:
        return {
            "project_id": project_id,
            "snapshots": [],
            "consolidated": {},
            "drift_log": [],
        }

    def load(self, project_id: int) -> Dict[str, Any]:
        path = self._path(project_id)
        if not os.path.exists(path):
            return self._defaults(project_id)
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)
        defaults = self._defaults(project_id)
        defaults.update(payload or {})
        defaults["project_id"] = project_id
        return defaults

    def save(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = self._defaults(project_id)
        payload.update(data or {})
        payload["project_id"] = project_id
        with open(self._path(project_id), "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        return payload

    def save_snapshot(self, project_id: int, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        data = self.load(project_id)
        data.setdefault("snapshots", []).append(snapshot)
        return self.save(project_id, data)

    def record_drift(self, project_id: int, drift_data: Dict[str, Any]) -> Dict[str, Any]:
        data = self.load(project_id)
        data.setdefault("drift_log", []).append(drift_data)
        return self.save(project_id, data)

    def update_consolidated(self, project_id: int, consolidated: Dict[str, Any]) -> Dict[str, Any]:
        data = self.load(project_id)
        data["consolidated"] = consolidated
        return self.save(project_id, data)
