from django.core.management.base import BaseCommand

from tasks.processor import TaskProcessor


class Command(BaseCommand):
    help = "Command to execute the scheduled tasks"

    def handle(self, *args, **kwargs):
        task_processor = TaskProcessor()
        task_processor.process_due_tasks()
