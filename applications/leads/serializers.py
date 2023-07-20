from rest_framework import serializers

from .models import Lead
from applications.account.models import Agent


class AgentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = "__all__"


class LeadModelSerializer(serializers.ModelSerializer):
    agent = AgentModelSerializer(many=True)

    class Meta:
        model = Lead
        fields = "__all__"
