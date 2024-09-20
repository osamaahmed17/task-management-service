import os
import json
import redis
import smtplib
from email import encoders
from fastapi import Depends
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from src.db.database import get_session
from src.api.task.models import Task
from sqlmodel import  select, Session
from email.mime.multipart import MIMEMultipart

redis_client = redis.Redis(host='localhost', port=6379, db=0)
load_dotenv()


class TaskService:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def get_tasks(self):
        statement = select(Task)
        tasks = self.session.exec(statement).all()
        
        return tasks
    
    def create_task(self, task_create_input):
        task = Task(**task_create_input.model_dump())

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
       
        try:
            # Access the environment variables
            smtp_host = os.getenv("SMTP_HOST")
            smtp_port = os.getenv("SMTP_PORT")
            mail_username = os.getenv("MAIL_USERNAME")
            mail_password = os.getenv("MAIL_PASSWORD")

            from_email = 'osamaahmed170395@gmail.com'
            mail_subject = "Task Created"
            mail_content_html = "Hello User <br/> A task has been created with the following information:<br/><ul><li>Tite: "+task.title+"</li><li>Description: "+task.description+"</li><li>Due Date: "+task.due_date+"</li></ul>  Feel free to contact support, if there are any questions!"
            to_email = "osamaahmed170395@gmail.com"
            self.sendEmail(smtp_host, smtp_port, mail_username, mail_password, from_email,
                    mail_subject,to_email, mail_content_html)
            print("Email has been sent successfully to the receiver's address.")
        except Exception as error:
            print("An error occurred:", error)
        redis_client.delete("tasks")
        redis_client.setex(f"task:{task.id}", 60 * 5, json.dumps(task.dict()))  # Cache for 5 minutes
        return task

    def sendEmail(self, smtp_host, smtp_port, mail_username, mail_password, from_email, mail_subject, to_email, mail_content_html):
        # create message object
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = from_email
        message['Subject'] = mail_subject
        message.attach(MIMEText(mail_content_html, 'html'))
        s = smtplib.SMTP(smtp_host, smtp_port)
        s.starttls()
        s.login(mail_username, mail_password)
        message_text = message.as_string()
        send_errors = s.sendmail(from_email, to_email, message_text)
        s.quit()
        if not len(send_errors.keys()) == 0:
            raise Exception("Errors occurred while sending email", send_errors)


    def get_by_id(self, task_id: int):
        print("hello there")
        cached_task = redis_client.get(f"task:{task_id}")
        if cached_task:
            print(f"Returning cached task {task_id}.")
            return json.loads(cached_task)

        statement = select(Task).where(Task.id == task_id)
        task = self.session.exec(statement).one_or_none()
        if task is None:
            raise Exception("Task not found")

        redis_client.setex(f"task:{task_id}", 60 * 5, json.dumps(task.dict()))  # Cache for 5 minutes

        return task

    def update_task(self, task_id, task_update_input):
        statement = select(Task).where(Task.id == task_id)
        task = self.session.exec(statement).one()
        for key, value in task_update_input.dict().items():
            setattr(task, key, value)
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        redis_client.delete(f"task:{task_id}")
        redis_client.delete("tasks")
        redis_client.setex(f"task:{task.id}", 60 * 5, json.dumps(task.dict()))  # Cache for 5 minutes
        return task

    def delete_task(self, task_id):
        statement = select(Task).where(Task.id == task_id)
        task = self.session.exec(statement).one()
        self.session.delete(task)
        self.session.commit()
        return task