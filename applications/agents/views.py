from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from applications.leads.models import Lead
from applications.leads.serializers import LeadModelSerializer
from .permissions import IsAssignedOrReadOnly
from rest_framework.response import Response
from rest_framework import status


class MyAssignedLeads(generics.RetrieveUpdateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadModelSerializer
    permission_classes = [IsAuthenticated, IsAssignedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
