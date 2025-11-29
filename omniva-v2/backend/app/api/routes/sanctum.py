"""Sanctum operator console endpoints."""

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.core.registry import registry

router = APIRouter(prefix="/sanctum", tags=["sanctum"])


class SanctumRequest(BaseModel):
    command: str


async def halo_sanctum_guard(request: Request) -> None:
    await registry.guard.require(request, "sanctum")


@router.post("/execute", dependencies=[Depends(halo_sanctum_guard)])
async def execute(request: SanctumRequest):
    return await registry.sanctum.execute(request.command)
