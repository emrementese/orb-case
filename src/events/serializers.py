from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer

from api.serializers import UserSerializer

from .models import Event


class EventSerializer(ModelSerializer):

    owner = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = "__all__"
        extra_kwargs = {
            "owner": {"read_only": True},
            "is_deleted": {"read_only": True},
        }

    def validate_date(self, value):
        if value < timezone.now().date():
            raise ValidationError("Date cannot be in the past")
        return value

    def validate_time(self, value):
        date = timezone.now().date()
        if self.initial_data["date"] == date and value < timezone.now().time():  # type: ignore
            raise ValidationError("Time cannot be in the past")
        return value

    def create(self, validated_data):
        request: Request = self.context["request"]
        validated_data["owner"] = request.user
        return super().create(validated_data)
