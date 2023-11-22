from django.core.exceptions import PermissionDenied
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response

from backend.users.auth import auth_token_for_user_credentials


class AuthTokenView(APIView):
    class AuthenticateRequestSerializer(serializers.Serializer):
        username = serializers.CharField(required=True)
        password = serializers.CharField(required=True)

    def _validate_post_data(self, post_data):
        auth_serializer = self.AuthenticateRequestSerializer(data=post_data)
        auth_serializer.is_valid(raise_exception=True)
        return auth_serializer.validated_data

    def post(self, request):
        try:
            validated_data = self._validate_post_data(post_data=request.POST)
            auth_token = auth_token_for_user_credentials(**validated_data)
            return Response(
                {"token": auth_token},
                status=status.HTTP_200_OK,
            )
        except serializers.ValidationError as e:
            return Response(
                {"error": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except PermissionDenied as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_403_FORBIDDEN,
            )
