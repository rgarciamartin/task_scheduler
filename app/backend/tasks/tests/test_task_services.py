from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from django.utils import timezone

from backend.tasks.services import create_task, list_tasks_for_user, delete_task
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
        TaskTestUtils.create_task(id=3, title="Test Task 2", owner_id=self.user.id)
        expected_tasks_ids_for_user = [3, 2]

        first_user_tasks_list = list_tasks_for_user(user_id=self.user.id)
        first_user_tasks_ids_list = list(first_user_tasks_list.values_list("id", flat=True))
        self.assertListEqual(expected_tasks_ids_for_user, first_user_tasks_ids_list)


class DeleteTaskTestCase(BaseTaskTestCase):
    def test_task_uuid_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Task uuid is required."):
            delete_task(task_uuid="", owner_id=self.user.id)

    def test_task_owner_is_required(self):
        with self.assertRaisesMessage(AssertionError, "Owner id is required."):
            delete_task(task_uuid=self.UUID, owner_id="")

    def test_not_owner_gets_permission_error(self):
        new_user = UserTestUtils.create_user(username="new_user", password="new")
        new_task = TaskTestUtils.create_task(id=2, title="Test Task 2", owner_id=new_user.id)

        with self.assertRaisesMessage(PermissionError, "User is not task owner."):
            delete_task(task_uuid=new_task.uuid, owner_id=self.user.id)

    def test_wrong_task_uuid_gets_not_exist_error(self):
        wrong_uuid = "ea0ec33b-30e2-9999-9011-e35e1e2b5e0d"

        with self.assertRaisesMessage(ObjectDoesNotExist, "Task matching query does not exist."):
            delete_task(task_uuid=wrong_uuid, owner_id=self.user.id)

    def test_task_deletion(self):
        TaskTestUtils.create_task(title="Test Task 1", owner_id=self.user.id)
        task_to_delete = TaskTestUtils.create_task(title="Test task deletion", owner_id=self.user.id)
        tasks_for_owner = TaskTestUtils.get_tasks_count_for_user(owner_id=self.user.id)
        self.assertEqual(tasks_for_owner, 2)

        delete_task(task_uuid=task_to_delete.uuid, owner_id=task_to_delete.owner.id)
        new_tasks_for_owner = TaskTestUtils.get_tasks_count_for_user(owner_id=self.user.id)
        self.assertEqual(new_tasks_for_owner, 1)
