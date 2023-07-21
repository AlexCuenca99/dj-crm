from rest_framework import serializers

from .models import Agent
from applications.account.serializers import UserSerializer


class AgentModelSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Agent
        fields = ["id", "organization", "user", "created", "modified"]


class AgentCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = [
            "user",
        ]

    def create(self, validated_data):
        organization = validated_data["user"].user_profile
        return Agent.objects.create(organization=organization, **validated_data)
