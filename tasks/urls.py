from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from tasks import views
from tasks.utils import require_valid_password

urlpatterns = [
    url(r"^$", RedirectView.as_view(permanent=True, url="dashboard/")),
    path(
        "dashboard/",
        require_valid_password(views.DashboardView.as_view()),
        name="dashboard",
    ),
    path("tasks/", require_valid_password(views.TaskView.as_view()), name="tasks"),
    path(
        "history/", require_valid_password(views.HistoryView.as_view()), name="history"
    ),
    url(r"^login/$", views.login, name="login"),
    url(r"^logout/$", views.logout, name="logout"),
    url(
        r"^cancel_task/(?P<task_id>.*?)$",
        views.CancelTaskView.as_view(),
        name="cancel_task",
    ),
]
