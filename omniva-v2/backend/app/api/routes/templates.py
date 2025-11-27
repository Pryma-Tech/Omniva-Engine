"""Template management API."""

from fastapi import APIRouter

from app.core.registry import registry
from app.models.template import StyleTemplate

router = APIRouter()


def _get_store():
    store = registry.get_subsystem("templates")
    if store is None:
        from app.subsystems.templates.template_store import TemplateStore

        store = TemplateStore()
    return store


@router.get("/")
async def list_templates() -> list:
    store = _get_store()
    return store.list_templates()


@router.post("/save")
async def save_template(data: dict) -> dict:
    store = _get_store()
    template = StyleTemplate(**data)
    return store.save_template(template)
