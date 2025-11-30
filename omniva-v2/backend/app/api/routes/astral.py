"""Astral multi-world futures API routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/astral.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/astral with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/astral with cognitive telemetry.

import logging

from fastapi import APIRouter, Depends, Request

from app.core.registry import registry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/astral", tags=["astral"])


async def halo_astral_guard(request: Request) -> None:
    await registry.guard.require(request, "nexus")


@router.get("/project/{project_id}", dependencies=[Depends(halo_astral_guard)])
async def future_branches(project_id: int):
    futures = registry.astral.alternate_futures(project_id)
    logger.info(
        "astral.future_branches",
        extra={"project_id": project_id, "branches": len(futures) if futures else 0},
    )
    return futures


@router.get("/snapshot", dependencies=[Depends(halo_astral_guard)])
async def snapshot():
    snap = registry.astral.astral_snapshot()
    logger.info("astral.snapshot", extra={"keys": list(snap.keys()) if isinstance(snap, dict) else None})
    return snap
