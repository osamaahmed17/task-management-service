from enum import Enum
from datetime import datetime
from pydantic import BaseModel, validator, ValidationError


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskCreateInput(BaseModel):
    title: str
    status: TaskStatus
    description: str
    due_date: str

    # Custom validator for due_date to ensure it follows DD/MM/YY format
    @validator("due_date")
    def check_due_date_format(cls, v):
        try:
            # Try to parse the date in the format DD/MM/YY
            datetime.strptime(v, "%d/%m/%y")
        except ValueError:
            raise ValueError("Due date must be in the format DD/MM/YY")
        return v

    @validator("status")
    def check_status(cls, v):
        if v not in ["pending", "in_progress", "completed"]:
            raise ValueError("Status must be 'pending', 'in_progress', or 'completed'")
        return v


class TaskUpdateInput(BaseModel):
    title: str
    status: str
    description: str
    due_date: str

    # Custom validator for due_date in update as well
    @validator("due_date")
    def check_due_date_format(cls, v):
        try:
            datetime.strptime(v, "%d/%m/%y")
        except ValueError:
            raise ValueError("Due date must be in the format DD/MM/YY")
        return v

