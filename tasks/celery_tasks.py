import logging
import time
from django.core.exceptions import ObjectDoesNotExist
from task_scheduler.celery_core import shared_task, app  # noimportqa
from .models import Task
from .utils import datetime_now

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def process_task(self, task_pk: int):
    """
    Process single task.

    :param int task_pk: Task to process
    """
    logger = logging.getLogger(__name__)

    try:
        task = Task.objects.get(id=task_pk)
    except ObjectDoesNotExist:
        logger.warning("Task %s not found", task_pk)
    task.status = Task.STATUS_INPROGRESS
    task.save()
    if task.is_long_running_task:
        time.sleep(60)
    print("Task is completed")
    task = Task.objects.get(id=task_pk)
    task.status = Task.STATUS_DONE
    task.executed_at = datetime_now()
    task.save()


def cancel_task(task_pk: int):
    """
    Cancel single task.

    :param int task_pk: Task to process
    """
    logger = logging.getLogger(__name__)

    try:
        task = Task.objects.get(id=task_pk)
    except ObjectDoesNotExist:
        logger.warning("Task %s not found", task_pk)
    if task.status == Task.STATUS_SCHEDULED:
        task.status = Task.STATUS_CANCELED
        task.save()
        return
    if task.status != Task.STATUS_INPROGRESS:
        logger.error(f"Can't cancel the task as status is {task.status}")
        return

    app.control.revoke(task.external_id.hex, terminate=True, signal="SIGKILL")
    task.status = Task.STATUS_CANCELED
    task.save()
