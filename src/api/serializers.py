from django.contrib.auth.models import User
from rest_framework import serializers


class NotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField(default="Bulunamadı.", read_only=True)


class UnAuthorizedSerializer(serializers.Serializer):
    detail = serializers.CharField(default="Giriş bilgileri verilmedi.", read_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
