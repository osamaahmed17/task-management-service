from fastapi import APIRouter, Depends
from src.api.task.schema import TaskCreateInput
from src.api.task.service import TaskService

router = APIRouter()

@router.get("/")
async def read_tasks(task_service : TaskService = Depends()):
    tasks = task_service.get_tasks()
    return tasks

@router.post("/")
async def create_task(task_create_input: TaskCreateInput, task_service : TaskService = Depends()):
    task = task_service.create_task(task_create_input)
    return task

@router.get("/{task_id}")
async def read_task(task_id: int, task_service: TaskService = Depends(), task: Mapping = Depends(get_task)):
    task = task_service.get_by_id(task_id)
    return task
    
    
@router.put("/{task_id}")
async def update_task(task_id: int, task_update_input: TaskUpdateInput, task_service: TaskService = Depends(), task: Mapping = Depends()):
    task = task_service.update(task_id, task_update_input)
    return task
    
@router.delete("/{task_id}")
async def delete_task(task_id: int, task_service : TaskService =Depends()):
    task = task_service.delete(task_id)
    return task