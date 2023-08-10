from rest_framework import serializers

from .models import Lead
from applications.agents.serializers import AgentModelSerializer
from .utils import send_email_lead_created


class LeadModelSerializer(serializers.ModelSerializer):
    agent = AgentModelSerializer(many=False)

    class Meta:
        model = Lead
        fields = "__all__"


class LeadCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = "__all__"

    def create(self, validated_data) -> Lead:
        lead = Lead.objects.create(**validated_data)
        send_email_lead_created(lead)
        return lead
