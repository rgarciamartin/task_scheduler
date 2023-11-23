from uuid import uuid4

from django.db import models
from django.core.exceptions import FieldError
from django.contrib.auth.models import User


class Task(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid4, editable=False)
    owner = models.ForeignKey(User, related_name="tasks", on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    class StatusChoices(models.TextChoices):
        TO_DO = "to_do", "To Do"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        STAND_BY = "stand_by", "Stand By"

    status = models.CharField(choices=StatusChoices.choices, max_length=20, default=StatusChoices.TO_DO)

    @classmethod
    def get_editable_fields(cls) -> list[str]:
        editable_fields = []
        for field in cls._meta.fields:
            if field.editable:
                editable_fields.append(field.name)
        return editable_fields

    @classmethod
    def validate_fields_are_editable(self, fields: list[str]) -> bool:
        editable_fields = self.get_editable_fields()
        all_fields_are_editable = all([field in editable_fields for field in fields])
        if not all_fields_are_editable:
            raise FieldError("Some fields cannot be updated.")

    def update_task_fields(self, **kwargs) -> None:
        updated_fields = []
        for field, value in kwargs.items():
            setattr(self, field, value)
            updated_fields.append(field)

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
