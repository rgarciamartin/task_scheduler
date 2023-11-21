import random
import string

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserTestUtils:
    @classmethod
    def generate_random_username(cls):
        RANDOM_SIZE = 15
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(RANDOM_SIZE))

    @classmethod
    def create_user(cls, username: str = None, email: str = None, password: str = None, **kwargs):
        username = username if username else cls.generate_random_username
        email = email if email else f"{username}@example.com"
        password = password if password else "test_pass"
        user = User.objects.create(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user


class AuthTokenTestUtils:
    @classmethod
    def create_auth_token_for_user(cls, user_id: int, **kwargs):
        return Token.objects.create(user_id=user_id)
