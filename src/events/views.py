from datetime import timedelta

from django.db.models import Q
from django.db.models.manager import BaseManager
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Event
from .serializers import EventSerializer


class EventViewSet(GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self) -> BaseManager[Event]:
        base_queryset = self.queryset.filter(is_deleted=False)
        match self.action:
            case "upcoming":
                last_24_hours = timezone.now() - timedelta(hours=24)
                upcoming_events = base_queryset.filter(
                    Q(date=last_24_hours.date(), time__gte=last_24_hours.time())
                )
                return upcoming_events
            case _:
                return base_queryset

    def list(self, request: Request, *args, **kwargs) -> Response:
        paginator = PageNumberPagination()
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=204)

    @extend_schema(
        summary="Get upcoming events",
        description="Get a list of upcoming events within the last 24 hours",
        responses={200: EventSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="upcoming", url_name="upcoming")
    def upcoming(self, request: Request, *args, **kwargs) -> Response:
        paginator = PageNumberPagination()
        queryset = self.get_queryset()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
