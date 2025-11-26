"""Task routes for Omniva Engine."""
# TODO: Manage pipeline tasks via API.

from typing import List, Optional

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from database.repository import TaskRepository
from utils.logger import logger


class TaskCreate(BaseModel):
    """Payload for creating a task."""

    task_type: str
    status: str = "pending"


class TaskUpdate(BaseModel):
    """Payload for updating task state."""

    task_type: Optional[str] = None
    status: Optional[str] = None


class TaskResponse(BaseModel):
    """Response schema for tasks."""

    id: int
    project_id: int
    task_type: str
    status: str

    class Config:
        orm_mode = True


router = APIRouter()
TASK_REPO = TaskRepository()


@router.get("/{project_id}", response_model=List[TaskResponse])
async def list_tasks(project_id: int, db: Session = Depends(get_db)) -> List[TaskResponse]:
    """
    List tasks for a project.
    TODO: Connect to TaskRepository.list().
    """
    logger.info("TODO: Implement listing tasks for project %s.", project_id)
    TASK_REPO.list(db)
    return []


@router.post(
    "/{project_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    project_id: int,
    payload: TaskCreate,
    db: Session = Depends(get_db),
) -> TaskResponse:
    """
    Create a task for a project.
    TODO: Persist via TaskRepository.create().
    """
    logger.info("TODO: Implement creating task for project %s.", project_id)
    TASK_REPO.create(db, data={"project_id": project_id, **payload.dict()})
    return TaskResponse(
        id=0,
        project_id=project_id,
        task_type=payload.task_type,
        status=payload.status,
    )
