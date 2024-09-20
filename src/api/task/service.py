from fastapi import Depends
from src.database import get_session
from src.api.task.models import Task
from sqlmodel import  select, Session


class TaskService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def get_tasks(self):
        statement = select(Task)
        tasks = self.session.exec(statement).all()
        return tasks
    
    def create_task(self, task_create_input):
        task = Task(**taskcreate_input.model_dump())
        print(task)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        if not self.session.contains(task):
            task = session.merge(task) 
        return task

    def get_by_id(self, task_id: int):
        statement = select(Task).where(Task.id == task_id)
        task = self.session.exec(statement).one_or_none()
        if task is None:
            raise Exception("Task not found")
        return task


    def update_task(self, task_id, task_update_input):
        statement = select(Task).where(Task.id == task_id)
        task = self.session.exec(statement).one()
        for key, value in task_update_input.dict().items():
            setattr(task, key, value)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task