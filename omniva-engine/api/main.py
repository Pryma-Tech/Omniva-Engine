"""Main entrypoint for the Omniva Engine API service."""

from fastapi import FastAPI

from config.settings import get_settings
from .routes import bot_control, config as config_routes, projects, uploads


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)


@app.on_event("startup")
async def on_startup() -> None:
    """Lifecycle hook for initializing infrastructure."""
    # TODO: Connect to the database, warm caches, and start workers.
    pass


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Lifecycle hook for gracefully shutting down dependencies."""
    # TODO: Close database connections and stop background services.
    pass


@app.get("/health", tags=["system"])
async def health_check() -> dict:
    """Report minimal API health information."""
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENV}


app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(bot_control.router, prefix="/bot", tags=["bot"])
app.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
app.include_router(config_routes.router, prefix="/config", tags=["config"])

# TODO: Add middleware, database dependencies, and authentication layers.
