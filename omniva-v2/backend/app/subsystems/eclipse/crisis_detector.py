"""Global crisis detection for Omniva Eclipse."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/subsystems/eclipse/crisis_detector.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/subsystems/eclipse/crisis_detector with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/subsystems/eclipse/crisis_detector with cognitive telemetry.


from __future__ import annotations

from datetime import datetime, timedelta
from typing import List


class CrisisDetector:
    """
    Uses Paradox, Infinity, Etherlink metrics to determine cascading failures.
    """

    def __init__(self, registry) -> None:
        self.registry = registry

    def scan(self) -> List[str]:
        paradox = self.registry.paradox.paradox_snapshot()
        inf = self.registry.infinity.infinity_snapshot()
        nodes = self.registry.node_registry.list()

        crisis_flags: List[str] = []

        for pid, anomalies in paradox.get("project_anomalies", {}).items():
            if len(anomalies) >= 2:
                crisis_flags.append(f"project_{pid}_multi_anomaly")

        if inf["load_score"] < 0.05 and inf["current_scale"] > 7:
            crisis_flags.append("infinity_unstable_scaling")

        for node_id, meta in nodes.items():
            last_seen = meta.get("last_seen")
            if last_seen:
                try:
                    stamp = datetime.fromisoformat(last_seen)
                    if datetime.utcnow() - stamp > timedelta(minutes=10):
                        crisis_flags.append(f"node_{node_id}_desync")
                except Exception:
                    continue

        return crisis_flags
