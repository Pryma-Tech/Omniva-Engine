"""Plugin management API routes."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.registry import registry

router = APIRouter(prefix="/forge", tags=["forge"])


class LoadPluginRequest(BaseModel):
    path: str


@router.get("/list")
async def list_plugins() -> dict:
    return registry.forge.list_plugins()


@router.post("/discover")
async def discover() -> list[str]:
    return registry.forge.discover()


@router.post("/load")
async def load_plugin(request: LoadPluginRequest):
    return registry.forge.load_plugin(request.path)


@router.post("/enable/{name}")
async def enable(name: str):
    return registry.forge.enable_plugin(name)


@router.post("/disable/{name}")
async def disable(name: str):
    return registry.forge.disable_plugin(name)
