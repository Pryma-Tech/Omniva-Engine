"""FastAPI entrypoint for Omniva Engine v2."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import load_config
from app.core.event_bus import event_bus
from app.core.plugins import load_plugins
from app.core.registry import initialize_all, list_subsystems, register_subsystem
from app.core.job_queue import get_job_queue
from app.api.routes import analysis as analysis_router
from app.api.routes import autonomous as autonomous_router
from app.api.routes import discovery as discovery_router
from app.api.routes import download as download_router
from app.api.routes import editing as editing_router
from app.api.routes import events as events_router
from app.api.routes import jobs as jobs_router
from app.api.routes import health as health_router
from app.api.routes import pipeline as pipeline_router
from app.api.routes import projects as projects_router
from app.api.routes import scheduler as scheduler_router
from app.api.routes import status as status_router
from app.api.routes import subsystems as subsystems_router
from app.api.routes import templates as templates_router
from app.api.routes import transcription as transcription_router
from app.api.routes import uploader as uploader_router
from app.api.routes import worker as worker_router
from app.api.routes import workers as workers_router
from app.subsystems.templates.template_store import TemplateStore
from app.subsystems.projects.project_manager import ProjectManager
from app.subsystems.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from app.subsystems.autonomous.autonomous_engine import AutonomousEngine
from app.subsystems.discovery.discovery_engine import DiscoveryEngine

config = load_config()
register_subsystem("templates", TemplateStore())
register_subsystem("project_manager", ProjectManager())
register_subsystem("orchestrator", PipelineOrchestrator())
register_subsystem("autonomous", AutonomousEngine())
register_subsystem("discovery", DiscoveryEngine())
load_plugins()
initialize_all()

async def global_event_logger(data: dict):
    print(f"[EVENT] {data}")


reliability_events = [
    "pipeline_started",
    "transcription_complete",
    "analysis_complete",
    "editing_complete",
    "upload_complete",
    "autonomous_pipeline_triggered",
    "discovery_new_posts",
    "job_retry_scheduled",
    "job_requeued",
    "job_timeout",
    "job_failed",
]


for evt in reliability_events:
    event_bus.subscribe(evt, global_event_logger)

app = FastAPI(title=config.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(status_router.router, prefix="/status", tags=["status"])
app.include_router(projects_router.router, prefix="/projects", tags=["projects"])
app.include_router(pipeline_router.router, prefix="/pipeline", tags=["pipeline"])
app.include_router(subsystems_router.router, prefix="/subsystems", tags=["subsystems"])
app.include_router(events_router.router, prefix="/events", tags=["events"])
app.include_router(jobs_router.router, prefix="/jobs", tags=["jobs"])
app.include_router(health_router.router, prefix="/health", tags=["health"])
app.include_router(discovery_router.router, prefix="/discover", tags=["discovery"])
app.include_router(autonomous_router.router, prefix="/autonomous", tags=["autonomous"])
app.include_router(transcription_router.router, prefix="/transcription", tags=["transcription"])
app.include_router(analysis_router.router, prefix="/analysis", tags=["analysis"])
app.include_router(download_router.router, prefix="/download", tags=["download"])
app.include_router(uploader_router.router, prefix="/uploader", tags=["uploader"])
app.include_router(editing_router.router, prefix="/editing", tags=["editing"])
app.include_router(scheduler_router.router, prefix="/scheduler", tags=["scheduler"])
app.include_router(templates_router.router, prefix="/templates", tags=["templates"])
app.include_router(worker_router.router, prefix="/worker", tags=["worker"])
app.include_router(workers_router.router, prefix="/workers", tags=["workers"])


@app.get("/info")
async def info() -> dict:
    return {
        "config": config.__dict__,
        "subsystems": list_subsystems(),
        "job_queue_length": len(get_job_queue()),
        "event_bus": "placeholder",
    }
