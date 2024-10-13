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

from api.serializers import NotFoundSerializer, UnAuthorizedSerializer

from .models import Event
from .serializers import EventSerializer


class EventViewSet(GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self) -> BaseManager[Event]:
        base_queryset = self.queryset.filter(is_deleted=False, owner=self.request.user)
        match self.action:
            case "upcoming":
                last_24_hours = timezone.now() - timedelta(hours=24)
                upcoming_events = base_queryset.filter(
                    Q(date=last_24_hours.date(), time__gte=last_24_hours.time())
                )
                return upcoming_events
            case _:
                return base_queryset

    @extend_schema(
        summary="Get a list of events",
        description="Get a list of all events",
        responses={
            200: EventSerializer(many=True),
            401: UnAuthorizedSerializer,
        },
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        paginator = PageNumberPagination()
        queryset = self.filter_queryset(self.get_queryset())
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    @extend_schema(
        summary="Get an event",
        description="Get an event by ID",
        responses={
            200: EventSerializer,
            401: UnAuthorizedSerializer,
            404: NotFoundSerializer,
        },
    )
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @extend_schema(
        summary="Create an event",
        description="Create an event",
        request=EventSerializer,
        responses={
            201: EventSerializer,
            401: UnAuthorizedSerializer,
        },
    )
    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    @extend_schema(
        summary="Update an event",
        description="Update an event by ID",
        request=EventSerializer,
        responses={
            200: EventSerializer,
            401: UnAuthorizedSerializer,
            404: NotFoundSerializer,
        },
    )
    def update(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        summary="Delete an event",
        description="Delete an event by ID",
        responses={204: None, 401: UnAuthorizedSerializer, 404: NotFoundSerializer},
    )
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=204)

    @extend_schema(
        summary="Get upcoming events",
        description="Get a list of upcoming events within the last 24 hours",
        responses={200: EventSerializer(many=True), 401: UnAuthorizedSerializer},
    )
    @action(detail=False, methods=["get"], url_path="upcoming", url_name="upcoming")
    def upcoming(self, request: Request, *args, **kwargs) -> Response:
        paginator = PageNumberPagination()
        queryset = self.get_queryset()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
