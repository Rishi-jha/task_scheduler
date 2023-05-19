import django_tables2 as tables
from django.utils.safestring import mark_safe
from django_celery_results.models import TaskResult

from tasks.models import Task


class DashboardTable(tables.Table):
    title = tables.Column(
        orderable=True,
        attrs={
            "td": {
                "class": "text-secondary text-xs font-weight-bold align-middle text-center"
            },
            "th": {
                "class": "text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
            },
        },
    )
    description = tables.Column(
        orderable=True,
        attrs={
            "td": {
                "class": "text-secondary text-xs font-weight-bold align-middle text-center"
            },
            "th": {
                "class": "text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
            },
        },
    )
    status = tables.Column(
        orderable=True,
        attrs={
            "td": {
                "class": "text-secondary text-xs font-weight-bold align-middle text-center"
            },
            "th": {
                "class": "text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
            },
        },
    )
    scheduled_at = tables.Column(
        orderable=True,
        attrs={
            "td": {
                "class": "text-secondary text-xs font-weight-bold align-middle text-center"
            },
            "th": {
                "class": "text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
            },
        },
    )
    executed_at = tables.Column(
        orderable=True,
        attrs={
            "td": {
                "class": "text-secondary text-xs font-weight-bold align-middle text-center"
            },
            "th": {
                "class": "text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
            },
        },
    )
    action = tables.Column(
        empty_values=(),
        orderable=False,
        attrs={
            "td": {
                "class": "text-secondary text-xs font-weight-bold align-middle text-center"
            },
            "th": {
                "class": "text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
            },
        },
    )

    class Meta:
        model = Task
        fields = (
            "title",
            "description",
            "status",
            "scheduled_at",
            "executed_at",
            "action",
        )
        attrs = {"class": "table align-items-center mb-0"}

    def render_action(self, record):
        if record.status == "scheduled" or record.status == "inprogress":
            return mark_safe(
                f'<button id="id_cancel_task" data-task-id= {record.id} type="button" class="cancel_task btn btn-outline-primary btn-sm mb-0">Cancel</button>'
            )
        else:
            return "--"


class HistoryTable(tables.Table):
    task_id = tables.Column(
        orderable=True,
        attrs={
            "td": {
                "class": "text-secondary text-xs font-weight-bold align-middle text-center"
            },
            "th": {
                "class": "text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
            },
        },
    )
    status = tables.Column(
        orderable=True,
        attrs={
            "td": {
                "class": "text-secondary text-xs font-weight-bold align-middle text-center"
            },
            "th": {
                "class": "text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
            },
        },
    )
    date_created = tables.Column(
        verbose_name="Created at",
        orderable=True,
        attrs={
            "td": {
                "class": "text-secondary text-xs font-weight-bold align-middle text-center"
            },
            "th": {
                "class": "text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
            },
        },
    )
    date_done = tables.Column(
        verbose_name="Completed at",
        orderable=True,
        attrs={
            "td": {
                "class": "text-secondary text-xs font-weight-bold align-middle text-center"
            },
            "th": {
                "class": "text-center text-uppercase text-secondary text-xxs font-weight-bolder opacity-7"
            },
        },
    )

    class Meta:
        model = TaskResult
        fields = (
            "task_id",
            "status",
            "date_created",
            "date_done",
        )
        attrs = {"class": "table align-items-center mb-0"}
