from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Agent

User = get_user_model()


class AgentTest(TestCase):
    """Test module for Agent model."""

    def setUp(self) -> None:
        """Set up a method which is used to initialize beofer any test run"""

        self.agent_info = self.generate_agent_info()

    def generate_agent_info(self) -> dict:
        """Generate agent info"""

        return {
            "email": "lakiboj883@royalka.com",
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
            "username": "AlexAgent",
            "password": "randompassword123",
            "role": "AGT",
        }

    def test_agent_user_creation(self):
        """

        Test for agent user creation.
        """

        # User creation
        user = User.objects.create_user(**self.agent_info)
        self.assertEqual(user.email, self.agent_info["email"])
        self.assertEqual(user.username, self.agent_info["username"])
        self.assertEqual(user.role, self.agent_info["role"])
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        # Get organization
        organization = user.user_profile

        # Agent creation
        agent = Agent.objects.create(organization=organization, user=user)
        agent_user = Agent.objects.get(user__username=self.agent_info["username"])

        self.assertEqual(agent.organization, organization)
        self.assertIsNotNone(agent_user)
