import logging
from datetime import timedelta

from tasks.celery_tasks import process_task
from tasks.models import Task
from tasks.utils import datetime_now

logger = logging.getLogger(__name__)


class TaskProcessor:
    """
    Picks up memos when their scheduled_at time has come.
    """

    @staticmethod
    def process_due_tasks():
        logger.info(
            "Querying for scheduled tasks where status=%s.",
            Task.STATUS_SCHEDULED,
        )
        tasks = Task.objects.filter(
            scheduled_at__lte=datetime_now(), status=Task.STATUS_SCHEDULED
        )
        logger.info("Found %s tasks.", tasks.count())

        for task in tasks:
            process_task.s(task.pk).apply_async(task_id=task.external_id.hex)
