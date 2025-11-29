"""Crisis protocol handling for autonomous safety."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/safety/crisis_protocols.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/safety/crisis_protocols with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/safety/crisis_protocols with cognitive telemetry.


from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from app.core.event_bus import event_bus


class CrisisProtocolEngine:
    """Pause autonomy and record diagnostics on failures."""

    def __init__(self, registry) -> None:
        self.registry = registry
        self.crises: Dict[int, List[Dict]] = {}

    def handle_exception(self, project_id: int, label: str, exc: Exception, trace: str | None = None) -> Dict:
        detail = {
            "time": datetime.utcnow().isoformat(),
            "label": label,
            "error": str(exc),
            "trace": trace,
        }
        self.crises.setdefault(project_id, []).append(detail)
        self.registry.autonomy.pause_project(project_id)
        intel = self.registry.get_subsystem("intelligence")
        if intel:
            intel.cognition.push_memory(project_id, {"crisis": detail})
        event_bus.publish("autonomy_crisis", {"project_id": project_id, **detail})
        return detail

    def get_crises(self, project_id: int) -> List[Dict]:
        return self.crises.get(project_id, [])
