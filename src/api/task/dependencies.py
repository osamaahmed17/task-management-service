from fastapi import HTTPException, Depends

from src.api.task.service import TaskService

def get_task(task_id: int, task_service: TaskService = Depends()):
    task = task_service.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="task not found")
    return task