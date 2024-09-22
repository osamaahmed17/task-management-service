from typing import Mapping
from src.api.task.models import Task
from fastapi import APIRouter, Depends
from src.api.task.schemas import TaskSchema
from src.api.task.service import TaskService


router = APIRouter()


@router.get(
    "/", summary="Fetch all the Tasks", description="This route fetches all the tasks"
)
async def read_tasks(task_service: TaskService = Depends()):
    tasks = task_service.get_tasks()
    return tasks


@router.get(
    "/{identifier}",
    summary="Fetch a specific task on either id or status",
    description="This route fetches all the tasks depending on the condition that are status or id",
)
async def read_task_or_status(identifier: str, task_service: TaskService = Depends()):
    print(identifier)
    # Check if the identifier is a valid integer (for task_id)
    if identifier.isdigit():
        task_id = int(identifier)
        task = task_service.get_by_id(task_id)
        if task:
            return task
        return {"error": "Task not found"}
    elif not identifier.isdigit():
        tasks = task_service.get_by_status(identifier)
        if tasks:
            return tasks
        return {"error": f"No tasks found with status '{identifier}'"}


@router.post(
    "/",
    summary="Creates a task",
    description="This route creates a task but requires a body as JSON",
)
async def create_task(
    task_create_input: TaskSchema, task_service: TaskService = Depends()
):
    task = task_service.create_task(task_create_input)
    return task


@router.put(
    "/{task_id}",
    summary="Updates a task",
    description="This route updates a task but requires an ID as param",
)
async def update_task(
    task_id: int,
    task_update_input: TaskSchema,
    task_service: TaskService = Depends(),
):
    task = task_service.update_task(task_id, task_update_input)
    return task


@router.delete(
    "/{task_id}",
    summary="Delete a task",
    description="This route delete a task but requires an ID as param",
)
async def delete_task(task_id: int, task_service: TaskService = Depends()):
    task = task_service.delete_task(task_id)
    return task
