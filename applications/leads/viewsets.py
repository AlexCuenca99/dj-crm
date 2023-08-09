from django.core.exceptions import ValidationError

from rest_framework import viewsets, status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from .models import Lead
from .utils import send_email_lead_created
from .permissions import IsOrganizerOrReadOnly
from .serializers import LeadModelSerializer, LeadCreateModelSerializer


class LeadModelViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadModelSerializer
    permission_classes = [IsOrganizerOrReadOnly]

    def get_serializer_class(self):
        if (
            self.action == "create"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            return LeadCreateModelSerializer
        else:
            return LeadModelSerializer

    @swagger_auto_schema(responses={201: LeadModelSerializer()})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        output_serializer = LeadModelSerializer

        if not serializer.is_valid():
            return Response(
                {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            output_serializer = LeadModelSerializer(serializer.save())
            send_email_lead_created(output_serializer.data)
        except Exception as e:
            raise ValidationError({"detail": e})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
