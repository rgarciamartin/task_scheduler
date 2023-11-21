from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token


def authenticate_user(username: str, password: str) -> str:
    assert username, "Username is required."
    assert password, "Password is required."

    user = authenticate(username=username, password=password)

    if user:
        auth_token, _ = Token.objects.get_or_create(user=user)
        return auth_token.key

    raise PermissionDenied("Incorrect username or password supplied.")
