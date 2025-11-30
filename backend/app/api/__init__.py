"""API router registration helpers."""

from fastapi import FastAPI

from .routes import heartbeat, orchestrator


def register_routes(app: FastAPI) -> None:
    """Attach all v0.1 routers to the FastAPI app."""
    app.include_router(heartbeat.router)
    app.include_router(orchestrator.router)

