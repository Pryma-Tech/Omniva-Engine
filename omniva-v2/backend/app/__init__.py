# TODO(omniva-v0.2): Extend omniva-v2/backend/app/__init__ with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/__init__ with cognitive telemetry.

"""Top-level package for the Omniva Engine v2 backend.

This module exposes the FastAPI application instance so callers can use
``from app import app`` as a stable import path.
"""

from .main import app

__all__ = ["app"]
