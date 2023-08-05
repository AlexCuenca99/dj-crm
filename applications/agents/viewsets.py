from django.core.exceptions import ValidationError

from rest_framework import viewsets, status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from .models import Agent
from applications.leads.permissions import IsOrganizer
from .serializers import AgentModelSerializer, AgentCreateModelSerializer


class AgentModelViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    permission_classes = [IsOrganizer]

    def get_serializer_class(self):
        if self.action == "create":
            return AgentCreateModelSerializer
        else:
            return AgentModelSerializer

    @swagger_auto_schema(responses={201: AgentModelSerializer()})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        output_serializer = AgentModelSerializer

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            output_serializer = AgentModelSerializer(self.perform_create(serializer))
        except Exception as e:
            raise ValidationError({"detail": e})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    # Send write_only data to the serializer using perform_create
    def perform_create(self, serializer, *args, **kwargs):
        return serializer.save(user=self.request.data["user"])
