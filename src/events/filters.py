from django_filters import rest_framework as filters

from .models import Event


class EventFilter(filters.FilterSet):
    filter_backends = [filters.DjangoFilterBackend]

    class Meta:
        model = Event
        fields = ["category", "date", "time"]
