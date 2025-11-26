"""FastAPI entrypoint for Omniva Engine v2."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import load_config
from .core.plugins import load_plugins
from .core.registry import list_subsystems, register_subsystem, initialize_all
from .core.job_queue import get_job_queue
from .core.event_bus import get_event_bus
from .api.routes import (
    projects,
    pipeline,
    subsystems,
    events,
    jobs,
    status,
    transcription,
    analysis,
    editing,
    uploader,
)

config = load_config()
load_plugins()
from .subsystems.analysis import AnalysisSubsystem
from .subsystems.editing import EditingSubsystem
from .subsystems.uploader import UploaderSubsystem
register_subsystem("analysis", AnalysisSubsystem())
register_subsystem("editing", EditingSubsystem())
register_subsystem("uploader", UploaderSubsystem())
initialize_all()

app = FastAPI(title=config.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(status.router, prefix="/status", tags=["status"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(pipeline.router, prefix="/pipeline", tags=["pipeline"])
app.include_router(subsystems.router, prefix="/subsystems", tags=["subsystems"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(transcription.router, prefix="/transcription", tags=["transcription"])
app.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
app.include_router(uploader.router, prefix="/uploader", tags=["uploader"])
app.include_router(editing.router, prefix="/editing", tags=["editing"])


@app.get("/info")
async def info() -> dict:
    return {
        "config": config.__dict__,
        "subsystems": list_subsystems(),
        "job_queue_length": len(get_job_queue()),
        "event_bus": "placeholder",
    }
