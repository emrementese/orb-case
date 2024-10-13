from django.contrib.auth import login
from drf_spectacular.utils import extend_schema
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    @extend_schema(
        request=AuthTokenSerializer,
        responses={200: AuthTokenSerializer},
    )
    def post(self, request, format=None) -> Response:
        # Giriş formunu işleme
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]  # type: ignore
        login(request, user)
        return super(LoginView, self).post(request, format=None)
