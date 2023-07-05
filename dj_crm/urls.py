from django.urls import path
from django.contrib import admin

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions


# Yasg Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="My Django CRM API",
        default_version="v1",
        description="API Docs for My Django CRM API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="alex-patricio1999@hotmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Base Urls
    path("admin/", admin.site.urls),
    # Yasg Urls
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
