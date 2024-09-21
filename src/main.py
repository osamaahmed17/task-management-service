from fastapi import FastAPI

from src.api.task.router import router as task_router

app = FastAPI(
    title="Task Management Application API",
    description="API for managing tasks including create, update, delete, and retrieve.",
    version="1.0",
)

app.include_router(task_router, prefix="/tasks", tags=["tasks"])
