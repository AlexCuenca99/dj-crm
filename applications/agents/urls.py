from django.urls import include, path

app_name = "agents_app"

urlpatterns = [path("", include("applications.agents.routers"))]
