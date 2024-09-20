from pydantic import BaseModel

class TaskCreateInput(BaseModel):
    title: str
    status: str
    description: str
    due_date: str


class TaskUpdateInput(BaseModel):
    title: str
    status: str
    description: str
    due_date: str
