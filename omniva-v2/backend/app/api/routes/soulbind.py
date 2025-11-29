# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/soulbind.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/soulbind with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/soulbind with cognitive telemetry.

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/soul", tags=["soul"])


@router.get("/codex")
async def codex():
    return registry.soul.get_codex()


@router.get("/journal")
async def journal():
    return registry.soul.get_journal()
