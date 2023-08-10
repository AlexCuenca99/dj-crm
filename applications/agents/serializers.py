from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Agent
from .utils import build_agent_email
from applications.account.serializers import (
    UserCustomSerializer,
    UserCreatePasswordRetypeCustomSerializer,
)

User = get_user_model()


class AgentModelSerializer(serializers.ModelSerializer):
    user = UserCustomSerializer()

    class Meta:
        model = Agent
        fields = ["id", "organization", "user", "created", "modified"]


class AgentCreateModelSerializer(serializers.ModelSerializer):
    user = UserCreatePasswordRetypeCustomSerializer()

    class Meta:
        model = Agent
        fields = [
            "user",
        ]

    def create(self, validated_data):
        # Create a new user using the Djoser Password retype serializer
        create_user_serializer = UserCreatePasswordRetypeCustomSerializer(
            data=validated_data["user"]
        )

        if create_user_serializer.is_valid(raise_exception=True):
            create_user_serializer.save()

        # Get created user
        user = User.objects.get(email=validated_data["user"]["email"])

        # Get created user organization
        organization = user.user_profile

        agent = Agent.objects.create(organization=organization, user=user)

        # Send email to created agent
        build_agent_email(agent)
        return agent
