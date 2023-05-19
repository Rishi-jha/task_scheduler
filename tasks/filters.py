from django_celery_results.models import TaskResult
from django_filters import FilterSet


class HistoryFilter(FilterSet):
    class Meta:
        model = TaskResult
        fields = {"status": ["exact"]}
