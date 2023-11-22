from typing import Optional

from django.db.models import QuerySet

from backend.tasks.models import Task
from .filters import TasksListFilter


def create_task(owner_id: int, **kwargs) -> Task:
    assert owner_id, "Owner id is required."
    task = Task(owner_id=owner_id, **kwargs)
    task.full_clean()
    task.save()
    return task


def list_tasks_for_user(user_id: int, query_params: Optional[dict] = None) -> QuerySet[Task]:
    assert user_id, "User id is required."
    tasks = Task.objects.filter(owner_id=user_id).order_by("-created")
    if query_params:
        tasks = TasksListFilter(query_params, tasks).qs
    return tasks
