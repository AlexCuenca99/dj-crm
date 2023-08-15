from django.urls import include, path
from .routers import router

app_name = "agents_app"

urlpatterns = [
    path("", include(router.urls)),
]
