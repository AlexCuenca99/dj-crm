from django.urls import include, path
from .views import MyAssignedLeadsRetrieveUpdateAPIView, MyAssignedLeadsListAPIView

app_name = "agents_app"

urlpatterns = [
    path("", include("applications.agents.routers")),
    path(
        "agents/my-assigned-leads/<pk>",
        MyAssignedLeadsRetrieveUpdateAPIView.as_view(),
        name="my-assigned-leads-detail",
    ),
    path(
        "agents/my-assigned-leads/",
        MyAssignedLeadsListAPIView.as_view(),
        name="my-assigned-leads-list",
    ),
]
