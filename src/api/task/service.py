import os
import json
import redis
import smtplib
from enum import Enum
from email import encoders
from fastapi import Depends
from datetime import datetime
from dotenv import load_dotenv
from fastapi import HTTPException
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from sqlmodel import select, Session
from src.api.task.models import Task
from src.db.database import get_session
from email.mime.multipart import MIMEMultipart

redis_client = redis.Redis(host= "localhost", port= 6379)
load_dotenv()


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def sendEmail(
        self,
        smtp_host,
        smtp_port,
        mail_username,
        mail_password,
        from_email,
        mail_subject,
        to_email,
        mail_content_html,
    ):
        message = MIMEMultipart()
        message["From"] = from_email
        message["To"] = from_email
        message["Subject"] = mail_subject
        message.attach(MIMEText(mail_content_html, "html"))
        s = smtplib.SMTP(smtp_host, smtp_port)
        s.starttls()
        s.login(mail_username, mail_password)
        message_text = message.as_string()
        send_errors = s.sendmail(from_email, to_email, message_text)
        s.quit()
        if not len(send_errors.keys()) == 0:
            raise HTTPException(
                status_code=400, detail=f"Errors occurred while sending email"
            )

    def get_tasks(self):
        cached_tasks = redis_client.get("task")
        total_task = 0
        if cached_tasks is not None:
            total_task = len(json.loads(cached_tasks)) 
        if cached_tasks:
            print("Fetching task from the cache")
            task = json.loads(cached_tasks)
            task = [Task(**task) for task in task]
        else:
            print("Fetching task from the database")
            statement = select(Task)
            task = self.session.exec(statement).all()
            task = [task.dict() for task in task]
            if cached_tasks is not None:
                    total_task = len(json.loads(cached_tasks))
            redis_client.set(
                "task", json.dumps(task), ex=60 * 5
            )  # Cache for 60 seconds
        total_task = f"total tasks: {total_task} "
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task, total_task

    def create_task(self, task_create_input):
        try:
            if not task_create_input.title.strip():
                raise HTTPException(status_code=400, detail="title cannot be empty.")

            if not task_create_input.description.strip():
                raise HTTPException(
                    status_code=400, detail="Description cannot be empty."
                )

            try:
                datetime.strptime(task_create_input.due_date, "%d/%m/%y")
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Due date must be in the format DD/MM/YY."
                )

            if task_create_input.status not in TaskStatus.__members__.values():
                raise HTTPException(
                    status_code=400,
                    detail="Status must be 'pending', 'in_progress', or 'completed'.",
                )

            task = Task(**task_create_input.model_dump())

            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)

            smtp_host = os.getenv("SMTP_HOST")
            smtp_port = os.getenv("SMTP_PORT")
            mail_username = os.getenv("MAIL_USERNAME")
            mail_password = os.getenv("MAIL_PASSWORD")
            from_email = "osamaahmed170395@gmail.com"
            mail_subject = "Task Created"
            mail_content_html = (
                f"Hello User <br/> A task has been created with the following information:<br/>"
                f"<ul><li>Title: {task.title}</li><li>Description: {task.description}</li>"
                f"<li>Due Date: {task.due_date}</li></ul>"
                "Feel free to contact support, if there are any questions!"
            )
            to_email = task.email
            self.sendEmail(
                smtp_host,
                smtp_port,
                mail_username,
                mail_password,
                from_email,
                mail_subject,
                to_email,
                mail_content_html,
            )

            print("Email has been sent successfully to the receiver's address.")

            redis_client.delete("task")
            redis_client.setex(
                f"task:{task.id}", 60 * 5, json.dumps(task.dict())
            )  # Cache for 5 minutes

        except HTTPException as http_error:
            raise http_error
        except Exception as error:
            raise HTTPException(
                status_code=400, detail=f"An error occurred: {str(error)}"
            )
        return task

    def get_by_id(self, task_id: int):
        cached_task = redis_client.get(f"task:{task_id}")
        if cached_task:
            print(f"Returning cached task {task_id}.")
            return json.loads(cached_task)

        statement = select(Task).where(Task.id == task_id)
        task = self.session.exec(statement).one_or_none()

        if not task:
            raise HTTPException(
                status_code=404, detail=f"Task with ID {task_id} not found"
            )
        return task

    def update_task(self, task_id, task_update_input):
        try:
            statement = select(Task).where(Task.id == task_id)

            task = self.session.exec(statement).one()
            task_data = task_update_input.dict()

            if not task_data.get("title").strip():
                raise HTTPException(status_code=400, detail="Title cannot be empty.")
            if not task_data.get("description").strip():
                raise HTTPException(
                    status_code=400, detail="Description cannot be empty."
                )
            if not task_data.get("due_date").strip():
                raise HTTPException(status_code=400, detail="Due date cannot be empty.")
            # Validate status
            status = task_data.get("status").strip()
            if not status:
                raise HTTPException(status_code=400, detail="Status cannot be empty.")
            if status not in TaskStatus.__members__.values():
                raise HTTPException(
                    status_code=400,
                    detail="Status must be 'pending', 'in_progress', or 'completed'.",
                )
            for key, value in task_update_input.dict().items():
                setattr(task, key, value)
            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)
            redis_client.flushdb()
            redis_client.setex(
                f"task:{task.id}", 60 * 5, json.dumps(task.dict())
            )  # Cache for 5 minutes
        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=f"There was an error while updating the task: {str(error)}",
            )
        print(task)
        return task

    def delete_task(self, task_id: int):
        try:
            statement = select(Task).where(Task.id == task_id)
            task = self.session.exec(statement).one()
            self.session.delete(task)
            self.session.commit()
            redis_client.delete(f"task:{task_id}")
            redis_client.flushdb()
     
        except Exception as error:
            raise HTTPException(
                status_code=400,
                detail=f"There was an error while updating the task: {str(error)}",
            )    
        return task

    def get_by_status(self, status: str):
        cached_tasks = redis_client.get("task")
        if cached_tasks:
            print("Fetching task from the cache")
            task = json.loads(cached_tasks)
            task = [task for task in task if task["status"] == status]
          # Cache for 60 second
        else:
            print("Fetching task from the database")
            statement = select(Task)
            task = self.session.exec(statement).all()
            task = [task.dict() for task in task]
            print(task)
            task = [task for task in task if task["status"] == status]
            redis_client.set(
                "task", json.dumps(task), ex=60 * 5
            )  # Cache for 60 seconds
        if not task:
            raise HTTPException(status_code=404, detail=f"Task not found")
        return task
