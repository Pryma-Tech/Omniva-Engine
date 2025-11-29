"""Filesystem-backed persistence for self-optimization runs."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/intelligence/self_opt/opt_store.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/intelligence/self_opt/opt_store with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/intelligence/self_opt/opt_store with cognitive telemetry.


import json
import os
from typing import Any, Dict


class SelfOptStore:
    """Persist optimizer runs and final weights per project."""

    def __init__(self) -> None:
        self.base = os.path.join("storage", "intelligence", "self_opt")
        os.makedirs(self.base, exist_ok=True)

    def _path(self, project_id: int) -> str:
        return os.path.join(self.base, f"{project_id}.json")

    def _defaults(self, project_id: int) -> Dict[str, Any]:
        return {
            "project_id": project_id,
            "runs": [],
            "final_weights": None,
        }

    def load(self, project_id: int) -> Dict[str, Any]:
        path = self._path(project_id)
        if not os.path.exists(path):
            return self._defaults(project_id)
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        defaults = self._defaults(project_id)
        defaults.update(data or {})
        defaults["project_id"] = project_id
        return defaults

    def save(self, project_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        payload = self._defaults(project_id)
        payload.update(data or {})
        payload["project_id"] = project_id
        with open(self._path(project_id), "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2)
        return payload

    def record_run(self, project_id: int, record: Dict[str, Any]) -> Dict[str, Any]:
        data = self.load(project_id)
        data.setdefault("runs", []).append(record)
        return self.save(project_id, data)

    def set_final_weights(self, project_id: int, weights: Dict[str, Any]) -> Dict[str, Any]:
        data = self.load(project_id)
        data["final_weights"] = weights
        return self.save(project_id, data)
