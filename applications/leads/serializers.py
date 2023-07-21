from rest_framework import serializers

from .models import Lead
from applications.agents.serializers import AgentModelSerializer


class LeadModelSerializer(serializers.ModelSerializer):
    agent = AgentModelSerializer(many=True)

    class Meta:
        model = Lead
        fields = "__all__"


class LeadCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = "__all__"
