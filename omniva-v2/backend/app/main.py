"""FastAPI entrypoint for Omniva Engine v2."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/main.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/main with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/main with cognitive telemetry.


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import load_config
from app.core.event_bus import event_bus
from app.core.plugins import load_plugins
from app.core.registry import initialize_all, list_subsystems, register_subsystem, registry
from app.core.job_queue import get_job_queue
from app.api.routes import analysis as analysis_router
from app.api.routes import autonomous as autonomous_router
from app.api.routes import discovery as discovery_router
from app.api.routes import download as download_router
from app.api.routes import editing as editing_router
from app.api.routes import events as events_router
from app.api.routes import jobs as jobs_router
from app.api.routes import health as health_router
from app.api.routes import intelligence as intelligence_router
from app.api.routes import autonomy as autonomy_router
from app.api.routes import safety as safety_router
from app.api.routes import governance as governance_router
from app.api.routes import federation as federation_router
from app.api.routes import meta as meta_router
from app.api.routes import orchestrator as orchestrator_router
from app.api.routes import heartbeat as heartbeat_router
from app.api.routes import constellation as constellation_router
from app.api.routes import observatory as observatory_router
from app.api.routes import strategy as strategy_router
from app.api.routes import identity as identity_router
from app.api.routes import soulbind as soul_router
from app.api.routes import archive as archive_router
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
from app.api.routes import sanctum as sanctum_router
from app.api.routes import forge as forge_router
from app.api.routes import etherlink as etherlink_router
from app.api.routes import halo as halo_router
from app.api.routes import oracle as oracle_router
from app.api.routes import astral as astral_router
from app.api.routes import infinity as infinity_router
from app.api.routes import paradox as paradox_router
from app.api.routes import eclipse as eclipse_router
from app.api.routes import stardust as stardust_router
from app.api.routes import lattice as lattice_router
from app.api.routes import horizon as horizon_router
from app.api.routes import pantheon as pantheon_router
from app.api.routes import chorus as chorus_router
from app.api.routes import halolux as halolux_router
from app.api.routes import zenith as zenith_router
from app.api.routes import safety as safety_router
from app.models import init_db
from app.subsystems.templates.template_store import TemplateStore
from app.subsystems.projects.project_manager import ProjectManager
from app.subsystems.orchestrator.pipeline_orchestrator import PipelineOrchestrator
from app.subsystems.autonomous.autonomous_engine import AutonomousEngine
from app.subsystems.discovery.discovery_engine import DiscoveryEngine
from app.subsystems.intelligence.intelligence_engine import IntelligenceEngine

config = load_config()
register_subsystem("templates", TemplateStore())
register_subsystem("project_manager", ProjectManager())
register_subsystem("orchestrator", PipelineOrchestrator())
register_subsystem("autonomous", AutonomousEngine())
register_subsystem("discovery", DiscoveryEngine())
register_subsystem("intelligence", IntelligenceEngine())
load_plugins()
initialize_all()
if config.database_url.startswith("sqlite"):
    init_db()

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

event_bus.subscribe("autonomous_discovered_links", global_event_logger)
event_bus.subscribe("autonomous_clip_downloaded", global_event_logger)
event_bus.subscribe("autonomous_transcribed", global_event_logger)
event_bus.subscribe("autonomous_analyzed", global_event_logger)
event_bus.subscribe("autonomous_scores_generated", global_event_logger)
event_bus.subscribe("autonomous_prioritized", global_event_logger)
event_bus.subscribe("autonomous_recommended", global_event_logger)
event_bus.subscribe("autonomous_uploaded", global_event_logger)
event_bus.subscribe("autonomous_scheduled", global_event_logger)
event_bus.subscribe("ghost_run_completed", global_event_logger)

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
app.include_router(autonomy_router.router, tags=["autonomy"])
app.include_router(safety_router.router, tags=["safety"])
app.include_router(governance_router.router, tags=["governance"])
app.include_router(federation_router.router, tags=["federation"])
app.include_router(meta_router.router, tags=["meta"])
app.include_router(orchestrator_router.router, tags=["orchestrator"])
app.include_router(heartbeat_router.router, tags=["heartbeat"])
app.include_router(constellation_router.router, tags=["constellation"])
app.include_router(observatory_router.router, tags=["observatory"])
app.include_router(strategy_router.router, tags=["strategy"])
app.include_router(identity_router.router, tags=["identity"])
app.include_router(soul_router.router, tags=["soul"])
app.include_router(archive_router.router, tags=["archive"])
app.include_router(transcription_router.router, prefix="/transcription", tags=["transcription"])
app.include_router(analysis_router.router, prefix="/analysis", tags=["analysis"])
app.include_router(download_router.router, prefix="/download", tags=["download"])
app.include_router(uploader_router.router, prefix="/uploader", tags=["uploader"])
app.include_router(editing_router.router, prefix="/editing", tags=["editing"])
app.include_router(scheduler_router.router, prefix="/scheduler", tags=["scheduler"])
app.include_router(templates_router.router, prefix="/templates", tags=["templates"])
app.include_router(worker_router.router, prefix="/worker", tags=["worker"])
app.include_router(workers_router.router, prefix="/workers", tags=["workers"])
app.include_router(sanctum_router.router)
app.include_router(forge_router.router)
app.include_router(etherlink_router.router)
app.include_router(halo_router.router)
app.include_router(oracle_router.router)
app.include_router(astral_router.router)
app.include_router(infinity_router.router)
app.include_router(paradox_router.router)
app.include_router(eclipse_router.router)
app.include_router(stardust_router.router)
app.include_router(lattice_router.router)
app.include_router(horizon_router.router)
app.include_router(pantheon_router.router)
app.include_router(chorus_router.router)
app.include_router(halolux_router.router)
app.include_router(zenith_router.router)
app.include_router(intelligence_router.router, prefix="/intelligence", tags=["intelligence"])
app.include_router(registry.forge.plugin_router)
app.include_router(registry.nexus.router)


@app.get("/info")
async def info() -> dict:
    return {
        "config": config.__dict__,
        "subsystems": list_subsystems(),
        "job_queue_length": len(get_job_queue()),
        "event_bus": "placeholder",
    }
