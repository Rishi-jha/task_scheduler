from http import HTTPStatus
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, override_settings

# Create your tests here.
from tasks.celery_tasks import process_task, cancel_task
from tasks.forms import TaskForm
from tasks.models import Task
from tasks.processor import TaskProcessor
from tasks.utils import datetime_now


class FunctionalTest(TestCase):
    def setUp(self):
        superuser = User.objects.create_superuser(
            "test", "test@api.com", "testpassword"
        )
        self.factory = RequestFactory()
        self.user = superuser
        self.client.login(username=superuser.username, password="testpassword")

    def test_add_new_task(self):
        tasks = Task.objects.count()
        self.assertEqual(tasks, 0)
        data = {
            "title": "Task1",
            "description": "Task 1 description",
            "scheduled_at": datetime_now(),
        }
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()
        tasks = Task.objects.count()
        self.assertEqual(tasks, 1)

    def test_scheduled_task_execution_change_status(self):
        self.test_add_new_task()
        task = Task.objects.get()
        task.status = Task.STATUS_SCHEDULED
        task.user = self.user
        task.save()
        process_task(task.pk)
        task = Task.objects.get()
        self.assertEqual(task.status, Task.STATUS_DONE)

    @mock.patch("tasks.celery_tasks.process_task.apply_async")
    def test_scheduled_task_execution_celery(self, mock_celery):
        self.test_add_new_task()
        task = Task.objects.get()
        task.status = Task.STATUS_SCHEDULED
        task.user = self.user
        task.save()
        task_processor = TaskProcessor()
        task_processor.process_due_tasks()
        mock_celery.assert_called_with((task.id,), {}, task_id=task.external_id.hex)

    def test_cancel_scheduled_task(self):
        self.test_add_new_task()
        task = Task.objects.get()
        task.status = Task.STATUS_SCHEDULED
        task.user = self.user
        task.save()
        cancel_task(task.pk)
        task = Task.objects.get()
        self.assertEqual(task.status, Task.STATUS_CANCELED)

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_cancel_in_progress_task(self):
        self.test_add_new_task()
        task = Task.objects.get()
        task.status = Task.STATUS_INPROGRESS
        task.user = self.user
        task.save()
        cancel_task(task.pk)
        task = Task.objects.get()
        self.assertEqual(task.status, Task.STATUS_CANCELED)
