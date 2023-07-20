from django.urls import include, path

app_name = "leads_app"

urlpatterns = [
    path("", include("applications.leads.routers")),
]
