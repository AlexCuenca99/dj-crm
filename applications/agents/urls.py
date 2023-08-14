from django.urls import include, path
from .views import MyAssignedLeadsRetrieveUpdateAPIView, MyAssignedLeadsListAPIView

app_name = "agents_app"

urlpatterns = [
    path("", include("applications.agents.routers")),
    path(
        "leads/my-assigned-leads/<pk>",
        MyAssignedLeadsRetrieveUpdateAPIView.as_view(),
        name="my-assigned-leads",
    ),
    path(
        "leads/my-assigned-leads/",
        MyAssignedLeadsListAPIView.as_view(),
        name="my-assigned-leads-list",
    ),
]
