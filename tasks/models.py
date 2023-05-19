import uuid
from datetime import time

from django.conf import settings
from django.db import models

# Create your models here.
import logging

from tasks.utils import datetime_now


logger = logging.getLogger(__name__)


class Task(models.Model):
    STATUS_SCHEDULED = "scheduled"
    STATUS_CANCELED = "canceled"
    STATUS_INPROGRESS = "inprogress"
    STATUS_DONE = "done"
    STATUS_CHOICES = [
        (STATUS_SCHEDULED, "Scheduled"),
        (STATUS_INPROGRESS, "In Progress"),
        (STATUS_DONE, "Completed"),
        (STATUS_CANCELED, "Canceled"),
    ]

    title = models.CharField(max_length=256)
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    description = models.TextField()
    scheduled_at = models.DateTimeField(default=datetime_now, db_index=True)
    executed_at = models.DateTimeField(db_index=True, null=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    is_long_running_task = models.BooleanField(
        default=False, verbose_name="Time Taking Task"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
