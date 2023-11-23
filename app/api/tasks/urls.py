from django.urls import path

from .views import TasksList, CreateTask, DeleteTask

urlpatterns = [
    path("list/", TasksList.as_view(), name="tasks_list"),
    path("create/", CreateTask.as_view(), name="create_task"),
    path("delete/<uuid:task_uuid>/", DeleteTask.as_view(), name="delete_task"),
]
