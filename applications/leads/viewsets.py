from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Lead
from .serializers import LeadModelSerializer


class LeadModelViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadModelSerializer
    permission_classes = [IsAdminUser]
