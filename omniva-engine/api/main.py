"""Main entrypoint for the Omniva Engine API service."""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from utils.logger import logger
from auth.dependencies import require_login
from config.settings import settings
from workers.manager import WorkerManager
from ai.prompt_engine import PromptEngine
from ai.templates.analysis import analysis_prompt
from ai.templates.editing import editing_prompt
from ai.templates.branding import branding_prompt
from ai.templates.metadata import metadata_prompt
from metadata.generator import MetadataGenerator
from projects.manager import ProjectManager
from projects.creators.manager import CreatorManager
from pipeline.orchestrator import ClipPipelineOrchestrator
from autonomous.manager import AutonomousModeManager
from pipeline.history.manager import PipelineHistoryManager
from errors.manager import ErrorManager
from pipeline.visualization.manager import PipelineVisualizationManager
from logs.manager import LogManager
from ffmpeg.processor import FFmpegProcessor
from storage.manager import StorageManager
from downloads.manager import DownloadManager
from transcription.manager import TranscriptionManager
from .routes import (
    auth as auth_routes,
    autonomous as autonomous_router,
    bot_control,
    branding as branding_router,
    clips,
    config as config_routes,
    creators,
    downloads as downloads_router,
    errors as errors_router,
    transcription as transcription_router,
    ffmpeg as ffmpeg_router,
    history as history_router,
    logs as logs_router,
    metadata as metadata_router,
    pipeline as pipeline_router,
    projects,
    prompts as prompts_router,
    storage as storage_router,
    tasks,
    uploads,
    videos,
    visualization as visualization_router,
    youtube as youtube_router,
)


worker_manager = WorkerManager()
prompt_engine = PromptEngine()
metadata_generator = MetadataGenerator(prompt_engine)
project_manager = ProjectManager()
creator_manager = CreatorManager()
clip_orchestrator = ClipPipelineOrchestrator(history=pipeline_history, errors=error_manager)
autonomous_manager = AutonomousModeManager()
pipeline_history = PipelineHistoryManager()
error_manager = ErrorManager()
pipeline_visualizer = PipelineVisualizationManager()
log_manager = LogManager()
ffmpeg_processor = FFmpegProcessor()
storage_manager = StorageManager()
download_manager = DownloadManager()
transcription_manager = TranscriptionManager()


def register_prompt_templates() -> None:
    """Register core prompt templates with the engine."""
    prompt_engine.register(analysis_prompt)
    prompt_engine.register(editing_prompt)
    prompt_engine.register(branding_prompt)
    prompt_engine.register(metadata_prompt)

templates = Jinja2Templates(directory="dashboard/pages")

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)
app.mount("/static", StaticFiles(directory="dashboard/static"), name="static")


@app.on_event("startup")
async def on_startup() -> None:
    """Lifecycle hook for initializing infrastructure."""
    logger.info("FastAPI Startup (placeholder)")
    logger.info("Loading runtime settings (placeholder)")
    _cfg = settings.load_secrets()
    app.state.worker_manager = worker_manager
    app.state.project_manager = project_manager
    app.state.creator_manager = creator_manager
    app.state.clip_orchestrator = clip_orchestrator
    app.state.autonomous_manager = autonomous_manager
    app.state.pipeline_history = pipeline_history
    app.state.error_manager = error_manager
    app.state.pipeline_visualizer = pipeline_visualizer
    app.state.log_manager = log_manager
    app.state.ffmpeg_processor = ffmpeg_processor
    app.state.storage_manager = storage_manager
    app.state.download_manager = download_manager
    app.state.transcription_manager = transcription_manager
    register_prompt_templates()
    # TODO: Connect to the database, warm caches, and start workers.


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Lifecycle hook for gracefully shutting down dependencies."""
    # TODO: Close database connections and stop background services.
    pass


@app.get("/health", tags=["system"])
async def health_check() -> dict:
    """Report minimal API health information."""
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENV}


@app.get("/", include_in_schema=False)
async def dashboard_home(request: Request):
    """Serve dashboard landing page."""
    require_login(request)
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/project-list", include_in_schema=False)
async def project_list_page(request: Request):
    """Serve project list page."""
    require_login(request)
    return templates.TemplateResponse("project_list.html", {"request": request})


@app.get("/project/{project_id}", include_in_schema=False)
async def project_detail(request: Request, project_id: int):
    """Serve project detail page."""
    require_login(request)
    return templates.TemplateResponse("project_detail.html", {"request": request, "project_id": project_id})


@app.get("/logs", include_in_schema=False)
async def logs_page(request: Request):
    """Serve dashboard log viewer."""
    require_login(request)
    return templates.TemplateResponse("logs.html", {"request": request})


@app.get("/storage", include_in_schema=False)
async def storage_page(request: Request):
    """Serve storage overview page."""
    require_login(request)
    return templates.TemplateResponse("storage.html", {"request": request})


@app.get("/branding", include_in_schema=False)
async def branding_page(request: Request):
    """Serve branding overview page."""
    require_login(request)
    return templates.TemplateResponse("branding.html", {"request": request})


@app.get("/youtube-setup", include_in_schema=False)
async def youtube_setup_page(request: Request):
    """Serve YouTube setup page."""
    require_login(request)
    return templates.TemplateResponse("youtube_setup.html", {"request": request})


app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(autonomous_router.router, prefix="/autonomous", tags=["autonomous"])
app.include_router(bot_control.router, prefix="/bot", tags=["bot"])
app.include_router(logs_router.router, prefix="/logs", tags=["logs"])
app.include_router(storage_router.router, prefix="/storage", tags=["storage"])
app.include_router(history_router.router, prefix="/history", tags=["history"])
app.include_router(prompts_router.router, prefix="/prompts", tags=["prompts"])
app.include_router(metadata_router.router, prefix="/metadata", tags=["metadata"])
app.include_router(pipeline_router.router, prefix="/pipeline", tags=["pipeline"])
app.include_router(downloads_router.router, prefix="/downloads", tags=["downloads"])
app.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
app.include_router(config_routes.router, prefix="/config", tags=["config"])
app.include_router(creators.router, prefix="/creators", tags=["creators"])
app.include_router(videos.router, prefix="/videos", tags=["videos"])
app.include_router(branding_router.router, prefix="/branding", tags=["branding"])
app.include_router(clips.router, prefix="/clips", tags=["clips"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(youtube_router.router, prefix="/youtube", tags=["youtube"])

# TODO: Add middleware, database dependencies, and authentication layers.
