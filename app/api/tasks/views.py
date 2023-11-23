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


class CreateTask(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    class CreateTaskSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField(required=False)
        status = serializers.CharField()

    def _validate_post_data(self, post_data) -> dict:
        task_data_serializer = self.CreateTaskSerializer(data=post_data)
        task_data_serializer.is_valid(raise_exception=True)
        return task_data_serializer.validated_data

    def post(self, request):
        try:
            validated_data = self._validate_post_data(post_data=request.POST)
            task = create_task(owner_id=request.user.id, **validated_data)
            return Response(
                {"task_uuid": str(task.uuid)},
                status=status.HTTP_201_CREATED,
            )

        except serializers.ValidationError as e:
            return Response(
                {"error": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UpdateTask(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    class UpdateTaskSerializer(serializers.Serializer):
        title = serializers.CharField()
        description = serializers.CharField(required=False)
        status = serializers.CharField()

    def _validate_post_data(self, post_data) -> dict:
        task_data_serializer = self.UpdateTaskSerializer(data=post_data)
        task_data_serializer.is_valid(raise_exception=True)
        return task_data_serializer.validated_data

    def post(self, request, task_uuid):
        try:
            validated_data = self._validate_post_data(post_data=request.POST)
            update_task(task_uuid=str(task_uuid), owner_id=request.user.id, **validated_data)
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )

        except ObjectDoesNotExist as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except PermissionError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN,
            )

        except serializers.ValidationError as e:
            return Response(
                {"error": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )


class DeleteTask(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, task_uuid):
        try:
            delete_task(task_uuid=str(task_uuid), owner_id=request.user.id)
            return Response(
                status=status.HTTP_204_NO_CONTENT,
            )

        except (ObjectDoesNotExist, PermissionError) as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
