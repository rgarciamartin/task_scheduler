from backend.tasks.services import (
    create_task,
    delete_task,
    update_task,
    list_tasks_for_user,
)
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class TasksList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    class TasksListSerializer(serializers.Serializer):
        uuid = serializers.UUIDField()
        title = serializers.CharField()
        created = serializers.DateTimeField()
        last_updated = serializers.DateTimeField()
        status = serializers.CharField()

    def get(self, request):
        tasks_list = list_tasks_for_user(user_id=request.user.id, query_params=request.GET)
        paginator = PageNumberPagination()
        paginated_tasks_list = paginator.paginate_queryset(tasks_list, request)
        return paginator.get_paginated_response(self.TasksListSerializer(paginated_tasks_list, many=True).data)
