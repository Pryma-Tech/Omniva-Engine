"""
Archive subsystem API routes.

These endpoints expose read-only access to the Omniva event/archive
timeline for dashboards and debugging tools.
"""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/archive.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/archive with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/archive with cognitive telemetry.

import logging

from fastapi import APIRouter

from app.core.registry import registry

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/archive", tags=["archive"])


@router.get("/timeline")
async def timeline():
    items = registry.archive.timeline[-200:]
    logger.info("archive.timeline", extra={"items": len(items)})
    return items


@router.get("/epochs")
async def epochs():
    epochs = registry.archive.epochs
    logger.info("archive.epochs", extra={"epochs": len(epochs)})
    return epochs


@router.get("/summary")
async def summary():
    data = registry.archive.summary()
    logger.info("archive.summary", extra={"keys": list(data.keys())})
    return data
