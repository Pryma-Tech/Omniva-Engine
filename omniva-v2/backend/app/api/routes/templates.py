"""Template subsystem API (placeholder)."""

from fastapi import APIRouter

from app.core.registry import registry
from app.models.template import StyleTemplate

router = APIRouter()


@router.get("/status")
async def template_status() -> dict:
    subsystem = registry.get_subsystem("templates")
    return subsystem.status()


@router.get("/list")
async def list_templates() -> list:
    subsystem = registry.get_subsystem("templates")
    return subsystem.list_templates()


@router.post("/add")
async def add_template(template: StyleTemplate) -> dict:
    subsystem = registry.get_subsystem("templates")
    return subsystem.add_template(template)


@router.get("/get/{name}")
async def get_template(name: str) -> dict:
    subsystem = registry.get_subsystem("templates")
    return subsystem.get_template(name)
