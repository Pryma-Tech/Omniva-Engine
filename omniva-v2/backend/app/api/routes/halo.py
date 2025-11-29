"""Halo security management routes."""

from fastapi import APIRouter, Depends, Request

from app.core.registry import registry

router = APIRouter(prefix="/halo", tags=["halo"])


async def halo_admin_guard(request: Request) -> None:
    await registry.guard.require(request, "sanctum")


@router.get("/tokens", dependencies=[Depends(halo_admin_guard)])
async def list_tokens():
    return {"tokens": registry.halo.get_core_tokens()}


@router.post("/rotate/{scope}", dependencies=[Depends(halo_admin_guard)])
async def rotate_token(scope: str):
    if scope not in registry.halo.get_core_tokens():
        return {"ok": False, "error": "unknown_scope"}
    return {"ok": True, "data": registry.halo.rotate_token(scope)}
