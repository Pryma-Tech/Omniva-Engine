"""Plugin management API routes."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/forge.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/forge with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/forge with cognitive telemetry.


from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel

from app.core.registry import registry

router = APIRouter(prefix="/forge", tags=["forge"])


class LoadPluginRequest(BaseModel):
    path: str


async def halo_plugin_guard(request: Request) -> None:
    await registry.guard.require(request, "plugin")


@router.get("/list", dependencies=[Depends(halo_plugin_guard)])
async def list_plugins() -> dict:
    return registry.forge.list_plugins()


@router.post("/discover", dependencies=[Depends(halo_plugin_guard)])
async def discover() -> list[str]:
    return registry.forge.discover()


@router.post("/load", dependencies=[Depends(halo_plugin_guard)])
async def load_plugin(request: LoadPluginRequest):
    return registry.forge.load_plugin(request.path)


@router.post("/enable/{name}", dependencies=[Depends(halo_plugin_guard)])
async def enable(name: str):
    return registry.forge.enable_plugin(name)


@router.post("/disable/{name}", dependencies=[Depends(halo_plugin_guard)])
async def disable(name: str):
    return registry.forge.disable_plugin(name)
