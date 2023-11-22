import django_filters as df
from backend.tasks.models import Task


class TasksListFilter(df.FilterSet):
    title = df.CharFilter(lookup_expr="icontains")
    status = df.ChoiceFilter(choices=Task.StatusChoices.choices)
    created_from = df.DateFilter(field_name="created", lookup_expr="date__gte")
    created_to = df.DateFilter(field_name="created", lookup_expr="date__lte")
