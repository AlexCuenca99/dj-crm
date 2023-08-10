from rest_framework import serializers

from .models import Lead
from applications.agents.serializers import AgentModelSerializer
from .utils import build_lead_email


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

        build_lead_email(lead)
        return lead
