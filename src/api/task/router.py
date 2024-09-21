from typing import Mapping
from fastapi import APIRouter, Depends
from src.api.task.service import TaskService
from src.api.task.dependencies import get_task
from src.api.task.schemas import TaskCreateInput, TaskUpdateInput

router = APIRouter()

@router.get("/")
async def read_tasks(task_service : TaskService = Depends()):
    tasks = task_service.get_tasks()
    return tasks

@router.get("/{identifier}")
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


@router.post("/")
async def create_task(task_create_input: TaskCreateInput, task_service : TaskService = Depends()):
    task = task_service.create_task(task_create_input)
    return task    
    
@router.put("/{task_id}")
async def update_task(task_id: int, task_update_input: TaskUpdateInput, task_service: TaskService = Depends()):
    task = task_service.update_task(task_id, task_update_input)
    return task
    
@router.delete("/{task_id}")
async def delete_task(task_id: int, task_service : TaskService = Depends()):
    task = task_service.delete_task(task_id)
    return task