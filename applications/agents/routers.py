from rest_framework import routers

from .viewsets import AgentModelViewSet


router = routers.DefaultRouter()
router.register(r"agents", AgentModelViewSet, basename="agents")

urlpatterns = router.urls
