import json
import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from sqlmodel import Session
from src.api.task.models import Task, TaskStatus
from src.api.task.service import TaskService

# Corrected the order of the mock arguments to match the decorators
@patch("smtplib.SMTP")
@patch("redis.Redis.delete")
def test_create_task_success(mock_redis_delete, mock_smtp):
    mock_session = MagicMock(spec=Session)å
    # Create task input as a Task instance with Enum member
    task_input = Task(
        title="Test Task",
        description="Task description",
        due_date="21/09/24",
        status=TaskStatus.pending  # Updated to use Enum member
    )

    task_service = TaskService(session=mock_session)
    task_service.redis = MagicMock()
    task_service.redis.delete = mock_redis_delete
    smtp_mock = mock_smtp.return_value
    smtp_mock.sendmail.return_value = {}
    task = task_service.create_task(task_input)
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    smtp_mock.sendmail.assert_called_once()
    mock_redis_delete.assert_called_once_with("task")


# Test for deleting a task successfully
def test_delete_task_success():
    task_mock = Task(id=1, title="Task to Delete")
    mock_session = MagicMock(spec=Session)
    mock_session.exec.return_value.one.return_value = task_mock
    task_service = TaskService(session=mock_session)
    task_service.redis = MagicMock()
    task_service.redis.delete = MagicMock()
    deleted_task = task_service.delete_task(1)
    mock_session.exec.assert_called_once()
    mock_session.delete.assert_called_once_with(task_mock)
    mock_session.commit.assert_called_once()
    assert deleted_task == task_mock
