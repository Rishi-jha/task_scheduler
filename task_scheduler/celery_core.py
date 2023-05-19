import sys, os

# noinspection PyUnresolvedReferences
from celery import Celery, shared_task  # noqa

from django.conf import settings


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_scheduler.settings")
app = Celery(__name__)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
