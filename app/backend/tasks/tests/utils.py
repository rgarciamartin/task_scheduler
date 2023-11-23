from backend.tasks.models import Task


class TaskTestUtils:
    @classmethod
    def create_task(cls, title: str, owner_id: int, **kwargs):
        return Task.objects.create(title=title, owner_id=owner_id, **kwargs)

    @classmethod
    def get_first_task_for_user(cls, owner_id: int, **kwargs):
        return Task.objects.filter(owner_id=owner_id, **kwargs).first()

    @classmethod
    def get_tasks_count_for_user(cls, owner_id: int, **kwargs):
        return Task.objects.filter(owner_id=owner_id, **kwargs).count()
