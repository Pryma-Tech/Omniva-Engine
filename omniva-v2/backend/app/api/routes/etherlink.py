"""Etherlink distributed deployment API routes."""
# TODO(omniva-v0.1): Implement core logic for omniva-v2/backend/app/api/routes/etherlink.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/etherlink with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/etherlink with cognitive telemetry.


from __future__ import annotations

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.registry import registry

router = APIRouter(prefix="/etherlink", tags=["etherlink"])


class RegisterRequest(BaseModel):
    node_id: str
    url: str
    roles: List[str]


class HeartbeatRequest(BaseModel):
    node_id: str


class EventRequest(BaseModel):
    topic: str
    payload: dict
    token: str


@router.post("/register")
async def register(request: RegisterRequest):
    return registry.etherlink.register_node(request.node_id, request.url, request.roles)


@router.post("/heartbeat")
async def heartbeat(request: HeartbeatRequest):
    return registry.etherlink.heartbeat(request.node_id)


@router.post("/event")
async def receive_event(request: EventRequest):
    if not registry.halo.validate(request.token, "etherlink"):
        return {"ok": False, "error": "unauthorized"}
    registry.eventbus.publish(request.topic, request.payload)
    return {"ok": True}


@router.get("/state")
async def get_state(token: str):
    if not registry.halo.validate(token, "etherlink"):
        return {"ok": False, "error": "unauthorized"}
    return registry.etherlink.local_state_snapshot()


@router.get("/nodes")
async def list_nodes():
    return registry.node_registry.list()
