from backend.users.auth import auth_token_for_user_credentials
from backend.users.tests.utils import AuthTokenTestUtils, UserTestUtils
from django.core.exceptions import PermissionDenied
from django.test import TestCase


class AuthenticateUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = UserTestUtils.create_user(username="test_user", password="test123")

    def test_username_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Username is required."):
            auth_token_for_user_credentials(username=None, password="test123")

    def test_password_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Password is required."):
            auth_token_for_user_credentials(username="test_user", password=None)

    def test_wrong_credentials_gets_permission_denied(self):
        with self.assertRaisesMessage(PermissionDenied, "Incorrect username or password supplied."):
            auth_token_for_user_credentials(username="test_user", password="pass")

    def test_authentication(self):
        auth_token = AuthTokenTestUtils.create_auth_token_for_user(user_id=self.user.id)
        received_token = auth_token_for_user_credentials(username="test_user", password="test123")
        self.assertEqual(auth_token.key, received_token)
