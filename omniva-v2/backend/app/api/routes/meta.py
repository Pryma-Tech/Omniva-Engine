"""Strategic meta-learning API routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/meta.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/meta with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/meta with cognitive telemetry.


from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/meta", tags=["meta"])


@router.get("/run")
async def run_meta() -> dict:
    return registry.meta.run_cycle() or {}
