from sqlmodel import Field, SQLModel
  
class Task(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: str
    status: str
    due_date: str
    create_at: str