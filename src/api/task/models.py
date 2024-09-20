from sqlmodel import Field, SQLModel
from datetime import datetime
  
class Task(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: str
    status: str
    description: str
    due_date: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
