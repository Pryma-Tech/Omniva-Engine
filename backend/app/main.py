"""FastAPI entrypoint for the minimal Omniva backend."""

from fastapi import FastAPI

from app.api import register_routes
from app.core.registry import registry

app = FastAPI(title="Omniva Engine Backend", version="0.1.0")
register_routes(app)


@app.get("/healthz", tags=["system"])
async def health_probe() -> dict:
    """Lightweight readiness probe."""
    projects = registry.get_subsystem("project_manager")
    return {
        "status": "ok",
        "heartbeat_running": registry.heartbeat.running if registry.heartbeat else False,
        "projects": projects.get_all_project_ids() if projects else [],
    }

