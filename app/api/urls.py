from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("auth/", include("api.auth.urls")),
    path("tasks/", include("api.tasks.urls")),
]
