"""Chorus emotional resonance API routes."""

from fastapi import APIRouter, Depends, Request

from app.core.registry import registry

router = APIRouter(prefix="/chorus", tags=["chorus"])


async def halo_chorus_guard(request: Request) -> None:
    await registry.guard.require(request, "nexus")


@router.get("/field", dependencies=[Depends(halo_chorus_guard)])
async def field():
    return registry.chorus.emotional_field()


@router.get("/modulation", dependencies=[Depends(halo_chorus_guard)])
async def modulation():
    return registry.chorus.modulation()


@router.get("/snapshot", dependencies=[Depends(halo_chorus_guard)])
async def snapshot():
    return registry.chorus.chorus_snapshot()
