"""Plugin loading (placeholder)."""
# TODO: Discover plugins dynamically from configuration.

import logging

from .registry import register_subsystem
from .event_bus import get_event_bus
from .job_queue import get_job_queue
from ..subsystems import downloader, scraper, transcription, analysis, editing, uploader, scheduler, templates, worker

logger = logging.getLogger("omniva_v2")


def load_plugins() -> None:
    """Initialize subsystem plugins and register them."""
    logger.info("Loading subsystem plugins (placeholder)")
    register_subsystem("event_bus", get_event_bus())
    register_subsystem("job_queue", get_job_queue())
    register_subsystem("downloader", downloader.DownloaderSubsystem())
    register_subsystem("scraper", scraper.ScraperSubsystem())
    register_subsystem("transcription", transcription.TranscriptionSubsystem())
    register_subsystem("analysis", analysis.AnalysisSubsystem())
    register_subsystem("editing", editing.EditingSubsystem())
    register_subsystem("uploader", uploader.UploaderSubsystem())
    register_subsystem("scheduler", scheduler.SchedulerSubsystem())
    register_subsystem("templates", templates.TemplateSubsystem())
    register_subsystem("worker", worker.WorkerSubsystem())
