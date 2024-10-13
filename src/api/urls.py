from django.urls import path, re_path
from drf_spectacular.views import SpectacularJSONAPIView as JsonView
from drf_spectacular.views import SpectacularSwaggerView as SwaggerView
from rest_framework import routers

api_router = routers.DefaultRouter()


urlpatterns = [
    # path("", include(api_router.urls)),
    path(
        "api/swagger-json",
        JsonView.as_view(),
        name="swagger-json",
    ),
    re_path(
        r"api/$",
        SwaggerView.as_view(url_name="swagger-json"),
        name="swagger-ui",
    ),
]
