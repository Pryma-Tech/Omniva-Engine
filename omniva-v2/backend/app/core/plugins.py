"""Subsystem plugin loader.

This module is responsible for importing and registering core subsystems
so they are available via the central registry.
"""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/core/plugins with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/core/plugins with cognitive telemetry.


import logging

from app.core.registry import register_subsystem
from app.core.event_bus import event_bus
from app.core.job_queue import job_queue

# Import subsystem modules for registration side effects.
from app.subsystems import (  # noqa: F401
    analysis,
    autonomous,
    downloader,
    editing,
    orchestrator,
    projects,
    scheduler,
    scraper,
    templates,
    transcription,
    uploader,
    worker,
)

logger = logging.getLogger("omniva_v2")


def load_plugins() -> None:
    """Initialize shared subsystems such as event bus and job queue."""
    logger.info("Loading subsystem plugins (placeholder)")
    register_subsystem("event_bus", event_bus)
    register_subsystem("job_queue", job_queue)
