from pydantic import BaseModel

class TaskCreateInput(BaseModel):
    title: str
    status: str
    due_date: str
    create_at: str


class TaskUpdateInput(BaseModel):
    title: str
    status: str
    due_date: str
    create_at: str