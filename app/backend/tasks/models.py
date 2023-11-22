from uuid import uuid4

from django.db import models
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

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
