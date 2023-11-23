from django.urls import path

from .views import TasksList, CreateTask

urlpatterns = [
    path("list/", TasksList.as_view(), name="tasks_list"),
    path("create/", CreateTask.as_view(), name="create_task"),
]
