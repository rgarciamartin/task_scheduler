from backend.tasks.models import Task


def create_task(owner_id: int, **kwargs) -> Task:
    assert owner_id, "Owner id is required."
    task = Task(owner_id=owner_id, **kwargs)
    task.full_clean()
    task.save()
    return task
