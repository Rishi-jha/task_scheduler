from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import views as auth_views

# Create your views here.
from django.urls import reverse
from django.contrib import messages
from django.views import generic
from django.views.generic import TemplateView, FormView, ListView
from django_celery_results.models import TaskResult
from django.db.models import TextField
from django.db.models.functions import Cast
from django_filters.views import FilterView
from django_tables2 import SingleTableView, SingleTableMixin

from tasks.celery_tasks import cancel_task
from tasks.filters import HistoryFilter
from tasks.forms import TaskForm
from tasks.models import Task
from tasks.tables import DashboardTable, HistoryTable


class DashboardView(SingleTableView):
    template_name = "tasks/dashboard.html"
    model = Task
    table_class = DashboardTable

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class TaskView(FormView):
    template_name = "tasks/task.html"
    success_message = "Task: {id} is created"
    form_class = TaskForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        user = self.request.user
        status = Task.STATUS_SCHEDULED
        obj.user = user
        obj.status = status
        obj.save()
        messages.info(self.request, self.success_message.format(id=obj.external_id.hex))
        return super(TaskView, self).form_valid(form)

    def get_success_url(self):
        return reverse("tasks")


class HistoryView(SingleTableMixin, FilterView):
    template_name = "tasks/history.html"

    model = TaskResult
    table_class = HistoryTable
    filterset_class = HistoryFilter

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        task_for_user = (
            Task.objects.filter(user=self.request.user)
            .annotate(str_id=Cast("external_id", output_field=TextField()))
            .values_list("str_id", flat=True)
        )
        qs = qs.filter(task_id__in=task_for_user)
        return qs


class CancelTaskView(generic.View):
    def post(self, request, **kwargs):
        cancel_task(kwargs["task_id"])
        return HttpResponse("Cancellation successful")


login = auth_views.LoginView.as_view()
logout = auth_views.LogoutView.as_view()
