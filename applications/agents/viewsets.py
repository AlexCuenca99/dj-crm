from django.core.exceptions import ValidationError

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema

from .models import Agent
from .permissions import IsAssignedOrReadOnly
from applications.leads.permissions import IsOrganizer
from applications.leads.models import Lead
from applications.leads.serializers import LeadModelSerializer
from .serializers import AgentModelSerializer, AgentCreateModelSerializer


class AgentModelViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()

    def get_permissions(self):
        if self.action == "create" or self.action == "delete":
            self.permission_classes = [IsOrganizer]
        elif (
            self.action == "update"
            or self.action == "partial_update"
            or self.action == "all_my_leads"
            or self.action == "my_leads"
        ):
            self.permission_classes = [IsAssignedOrReadOnly]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return AgentCreateModelSerializer
        elif self.action == "all_my_leads" or self.action == "my_leads":
            return LeadModelSerializer
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

    @swagger_auto_schema(
        method="get",
        responses={200: LeadModelSerializer()},
    )
    @action(
        detail=False,
        methods=[
            "get",
        ],
        url_path="my-leads",
    )
    def all_my_leads(self, request):
        user = request.user
        leads = Lead.objects.filter(agent__user=user)
        serializer = self.get_serializer(leads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method="patch",
        request_body=LeadModelSerializer,
        responses={200: LeadModelSerializer()},
        operation_description="Update the lead you were assigned",
    )
    @action(
        detail=False,
        methods=[
            "patch",
        ],
        url_path="my-leads/(?P<lead_pk>[^/.]+)",
    )
    def my_leads(self, request, lead_pk=None, *args, **kwargs):
        lead = Lead.objects.get(id=lead_pk)
        self.check_object_permissions(request, obj=lead)
        serializer = self.get_serializer(lead, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
