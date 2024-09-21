from sqlmodel import Field, SQLModel
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
  
class Task(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: str
    status: TaskStatus
    description: str
    due_date: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
