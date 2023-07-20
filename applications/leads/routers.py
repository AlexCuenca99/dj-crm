from rest_framework import routers

from .viewsets import LeadModelViewSet

router = routers.DefaultRouter()
router.register(r"leads", LeadModelViewSet, basename="leads")

urlpatterns = router.urls
