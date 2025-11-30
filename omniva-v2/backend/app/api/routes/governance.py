"""Governance policy API."""
# DONE(omniva-v0.1): Core logic implemented for omniva-v2/backend/app/api/routes/governance.
# TODO(omniva-v0.2): Extend omniva-v2/backend/app/api/routes/governance with advanced behaviors.
# TODO(omniva-v0.3): Integrate omniva-v2/backend/app/api/routes/governance with cognitive telemetry.


from fastapi import APIRouter

from app.core.registry import registry

router = APIRouter(prefix="/governance", tags=["governance"])


@router.get("/policy/{project_id}")
async def get_policy(project_id: int) -> dict:
    return registry.policy_model.get_policy(project_id)


@router.post("/policy/{project_id}")
async def update_policy(project_id: int, payload: dict) -> dict:
    payload = payload or {}
    return registry.policy_model.update_policy(project_id, payload)
