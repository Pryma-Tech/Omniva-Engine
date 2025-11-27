"""
Pipeline orchestrator subsystem.
"""

from typing import Any, Dict, List

from app.core.event_bus import event_bus
from app.core.job_queue import job_queue
from app.core.registry import registry


class PipelineOrchestrator:
    """Kick off full pipeline runs for a project."""

    name = "orchestrator"

    def initialize(self) -> Dict[str, str]:
        return {"status": "pipeline orchestrator initialized"}

    def run_pipeline(self, project_id: int, creators: List[str]) -> Dict[str, Any]:
        for link in creators:
            job_queue.enqueue(
                "download_url",
                {
                    "url": link,
                    "project_id": project_id,
                },
            )

        event_bus.publish(
            "pipeline_started",
            {"project_id": project_id, "creators": creators},
        )
        return {"status": "pipeline started", "project_id": project_id, "creators": creators}

    def status(self) -> Dict[str, str]:
        return {"name": self.name, "status": "ok"}
