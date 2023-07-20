from rest_framework import viewsets

from .models import Lead
from .permissions import IsOrganizerOrReadOnly
from .serializers import LeadModelSerializer, LeadCreateModelSerializer


class LeadModelViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadModelSerializer
    permission_classes = [IsOrganizerOrReadOnly]

    def get_serializer_class(self):
        if self.action == "create":
            return LeadCreateModelSerializer
        else:
            return LeadModelSerializer
