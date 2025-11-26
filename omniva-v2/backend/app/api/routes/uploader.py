"""Uploader subsystem API (placeholder)."""

from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter()


@router.get("/status")
async def uploader_status() -> dict:
    subsystem = registry.get_subsystem("uploader")
    return subsystem.status()


@router.post("/upload")
async def manual_upload(data: dict) -> dict:
    subsystem = registry.get_subsystem("uploader")
    renders = data.get("renders", [])
    return subsystem.upload(renders)
