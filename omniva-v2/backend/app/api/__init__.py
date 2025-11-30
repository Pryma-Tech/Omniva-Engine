"""API package for Omniva Engine v2.

This package hosts the HTTP API surface for the Omniva Engine backend.
For now it primarily serves as a namespace for :mod:`app.api.routes`,
which contains the concrete FastAPI routers used in :mod:`app.main`.

Higher-level orchestration (e.g. a versioned top-level router) can be
added in future iterations.
"""

# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/__init__ with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/__init__ with cognitive telemetry.

from . import routes

__all__ = ["routes"]
