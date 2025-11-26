"""Prompt API routes."""
# TODO: Add authentication and richer filtering.

from fastapi import APIRouter

from ai.prompt_engine import prompt_engine

router = APIRouter()


@router.get("/{name}")
async def get_prompt(name: str) -> dict:
    """Return prompt template text."""
    tmpl = prompt_engine.get(name)
    return {"template": tmpl.template if tmpl else None}


@router.post("/{name}")
async def render_prompt(name: str, data: dict) -> dict:
    """Render prompt output."""
    return {"rendered": prompt_engine.render(name, **data)}
