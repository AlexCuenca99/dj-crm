from django.urls import include, path
from .views import MyAssignedLeads

app_name = "agents_app"

urlpatterns = [
    path("", include("applications.agents.routers")),
    path(
        "leads/my-assigned-leads/<pk>",
        MyAssignedLeads.as_view(),
        name="my-assigned-leads",
    ),
]
