from django.forms import ModelForm

from tasks.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "scheduled_at",
            "is_long_running_task",
        )
