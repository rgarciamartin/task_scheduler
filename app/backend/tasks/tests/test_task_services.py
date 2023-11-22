from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.test import TestCase
from django.utils import timezone

from backend.tasks.services import create_task
from backend.users.tests.utils import UserTestUtils

from .utils import TaskTestUtils


class BaseTaskTestCase(TestCase):
    UUID = "ea0ec33b-30e2-4601-9011-e35e1e2b5e0d"

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = UserTestUtils.create_user(username="test@example.com", password="test123")
        return super().setUpTestData()


class CreateTaskTestCase(BaseTaskTestCase):
    def test_owner_id_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Owner id is required."):
            create_task(owner_id="", task_data={})

    def test_invalid_status_raises_validation_error(self):
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": "not_valid",
        }
        with self.assertRaises(ValidationError):
            create_task(owner_id=self.user.id, **task_data)

    def test_create_task(self):
        task_data = {
            "title": "Test Task",
            "description": "Test description",
            "status": "stand_by",
        }

        create_task(owner_id=self.user.id, **task_data)
        self.assertIsNotNone(TaskTestUtils.get_first_task_for_user(owner_id=self.user.id, **task_data))
