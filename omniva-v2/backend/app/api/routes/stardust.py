"""Stardust provenance API routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.core.registry import registry

router = APIRouter(prefix="/stardust", tags=["stardust"])


class PacketRequest(BaseModel):
    ptype: str
    payload: dict
    parents: Optional[List[str]] = None


async def halo_stardust_guard(request: Request) -> None:
    await registry.guard.require(request, "nexus")


@router.post("/packet", dependencies=[Depends(halo_stardust_guard)])
async def create_packet(body: PacketRequest):
    return registry.stardust.create_packet(body.ptype, body.payload, body.parents)


@router.get("/trace/{packet_id}", dependencies=[Depends(halo_stardust_guard)])
async def trace(packet_id: str):
    return registry.stardust.trace(packet_id)


@router.get("/influence/{packet_id}", dependencies=[Depends(halo_stardust_guard)])
async def influence(packet_id: str):
    return registry.stardust.influence(packet_id)


@router.get("/graph", dependencies=[Depends(halo_stardust_guard)])
async def graph():
    return registry.stardust.graph_snapshot()
