from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from applications.leads.models import Lead
from applications.leads.serializers import LeadModelSerializer
from .permissions import IsAssignedOrReadOnly
from rest_framework.response import Response
from rest_framework import status


class MyAssignedLeadsRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadModelSerializer
    permission_classes = [IsAuthenticated, IsAssignedOrReadOnly]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyAssignedLeadsListAPIView(generics.ListAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadModelSerializer
    permission_classes = [IsAuthenticated, IsAssignedOrReadOnly]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(agent_user__email=request.user_email)
        print("QUERY_SET -> ", queryset, end="\n\n")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
