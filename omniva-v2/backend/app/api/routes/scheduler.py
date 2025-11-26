"""Scheduler API routes (placeholder)."""

from fastapi import APIRouter

from app.core.registry import registry
from app.models.scheduler import ScheduleRule

router = APIRouter()


@router.get("/status")
async def scheduler_status() -> dict:
    subsystem = registry.get_subsystem("scheduler")
    return subsystem.status()


@router.get("/rules")
async def list_rules() -> list:
    subsystem = registry.get_subsystem("scheduler")
    return subsystem.list_rules()


@router.post("/add")
async def add_rule(rule: ScheduleRule) -> dict:
    subsystem = registry.get_subsystem("scheduler")
    return subsystem.add_rule(rule)


@router.post("/evaluate")
async def evaluate_rules() -> dict:
    subsystem = registry.get_subsystem("scheduler")
    return subsystem.evaluate_schedules()


@router.post("/trigger/{project_id}")
async def trigger_pipeline(project_id: int) -> dict:
    subsystem = registry.get_subsystem("scheduler")
    return subsystem.trigger_pipeline(project_id)
