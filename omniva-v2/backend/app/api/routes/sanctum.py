"""Sanctum operator console endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.registry import registry

router = APIRouter(prefix="/sanctum", tags=["sanctum"])


class SanctumRequest(BaseModel):
    command: str


@router.post("/execute")
async def execute(request: SanctumRequest):
    return await registry.sanctum.execute(request.command)
