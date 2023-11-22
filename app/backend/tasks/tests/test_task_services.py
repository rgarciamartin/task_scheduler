from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from django.utils import timezone

from backend.tasks.services import create_task, list_tasks_for_user
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


class ListTasksForUserTestCase(BaseTaskTestCase):
    def test_service_returns_a_queryset(self):
        tasks_list = list_tasks_for_user(user_id=self.user.id)
        self.assertIs(type(tasks_list), QuerySet)

    def test_owner_id_is_required(self):
        with self.assertRaisesMessage(AssertionError, "User id is required."):
            list_tasks_for_user(user_id="")

    def test_list_only_user_tasks(self):
        new_user = UserTestUtils.create_user(username="new_user", password="new")
        TaskTestUtils.create_task(id=1, title="Other user task", owner_id=new_user.id)
        TaskTestUtils.create_task(id=2, title="Test Task 1", owner_id=self.user.id)
        TaskTestUtils.create_task(id=3, title="Test Task 1", owner_id=self.user.id)
        expected_tasks_ids_for_user = [3, 2]

        first_user_tasks_list = list_tasks_for_user(user_id=self.user.id)
        first_user_tasks_ids_list = list(first_user_tasks_list.values_list("id", flat=True))
        self.assertListEqual(expected_tasks_ids_for_user, first_user_tasks_ids_list)
