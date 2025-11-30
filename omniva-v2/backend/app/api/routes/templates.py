"""Template management API."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/templates.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/templates with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/templates with cognitive telemetry.


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
