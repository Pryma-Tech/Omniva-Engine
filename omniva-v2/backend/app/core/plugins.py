"""Subsystem plugin loader (placeholder)."""

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
