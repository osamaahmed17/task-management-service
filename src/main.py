from fastapi import FastAPI

from src.api.task.router import router as task_router

app = FastAPI()

app.include_router(task_router, prefix="/tasks", tags=["tasks"])
