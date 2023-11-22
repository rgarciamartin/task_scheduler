from api.auth.views import AuthTokenView
from backend.users.tests.utils import AuthTokenTestUtils, UserTestUtils
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTokenViewTestCase(APITestCase):
    endpoint_url = "/api/v1/auth/token/"

    def test_view_url(self):
        response = self.client.post(self.endpoint_url)
        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIs(response.resolver_match.func.view_class, AuthTokenView)

    def test_get_method_gets_405_error(self):
        response = self.client.get(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_method_gets_405_error(self):
        response = self.client.put(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_method_gets_405_error(self):
        response = self.client.delete(self.endpoint_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_invalid_credentials_gets_403_error(self):
        post_data = {"username": "user", "password": "pass"}
        expected_error = "Incorrect username or password supplied."

        response = self.client.post(self.endpoint_url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json().get("error"), expected_error)

    def test_username_and_password_are_required(self):
        post_data = {}
        expected_error = {
            "username": ["Este campo es requerido."],
            "password": ["Este campo es requerido."],
        }

        response = self.client.post(self.endpoint_url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json().get("error"), expected_error)

    def test_username_and_password_cannot_be_blank(self):
        post_data = {"username": "", "password": ""}
        expected_error = {
            "username": ["Este campo no puede estar en blanco."],
            "password": ["Este campo no puede estar en blanco."],
        }

        response = self.client.post(self.endpoint_url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json().get("error"), expected_error)

    def test_view_gets_expected_response(self):
        USERNAME = "test_user"
        PASSWORD = "test123"
        user = UserTestUtils.create_user(username=USERNAME, password=PASSWORD)
        auth_token = AuthTokenTestUtils.create_auth_token_for_user(user_id=user.id)
        post_data = {"username": USERNAME, "password": PASSWORD}

        response = self.client.post(self.endpoint_url, data=post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("token"), auth_token.key)
