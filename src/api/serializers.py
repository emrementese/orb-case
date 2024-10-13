from rest_framework import serializers


class NotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField(default="Bulunamadı.", read_only=True)


class UnAuthorizedSerializer(serializers.Serializer):
    detail = serializers.CharField(default="Giriş bilgileri verilmedi.", read_only=True)
