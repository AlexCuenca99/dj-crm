ORGANIZER_TEST_EMAIL_ADDRESS = "alex@alex.com"
AGENT_TEST_EMAIL_ADDRESS = "mafoh16227@touchend.com"

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test.utils import override_settings

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Agent
from ..serializers import AgentModelSerializer

User = get_user_model()


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend", DEBUG=True
)
class GetAllAgentsTest(APITestCase):
    def setUp(self) -> None:
        """Set up a method which is used to initialize before any test run"""
        self.agent_info = self.generate_agent_info()
        self.organizer_info = self.generate_organizer_info()

    def generate_agent_info(self) -> dict:
        """Generate agent info"""
        return {
            "email": AGENT_TEST_EMAIL_ADDRESS,
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
            "username": "AlexAgent",
            "password": "randompassword123",
            "re_password": "randompassword123",
            "role": "AGT",
        }

    def generate_organizer_info(self) -> dict:
        """Generate organizer info"""

        return {
            "email": ORGANIZER_TEST_EMAIL_ADDRESS,
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
            "username": "AlexOrganizer",
            "password": "randompassword123",
            "re_password": "randompassword123",
            "role": "ORG",
        }

    def test_get_all_agents(self):
        """Test for getting all agents using API"""

        # Create and activatye an organizer user
        url = reverse("customuser-list")
        response = self.client.post(url, self.organizer_info)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        organizer_user = User.objects.get(username=self.organizer_info["username"])
        organizer_user.is_active = True
        organizer_user.save()

        # Login organizer user and get token
        url = reverse("jwt-create")
        organizer_login_data = {
            "email": self.organizer_info["email"],
            "password": self.organizer_info["password"],
        }

        response = self.client.post(url, organizer_login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["access"])

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Agent creation
        url = reverse("agents_app:agents-list")
        response = self.client.get(url)

        agents = Agent.objects.all()
        serializer = AgentModelSerializer(agents, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateSingleAgentTest(APITestCase):
    def setUp(self) -> None:
        """Set up a method which is used to initialize before any test run"""
        self.agent_info = self.generate_agent_info()
        self.organizer_info = self.generate_organizer_info()

    def generate_agent_info(self) -> dict:
        """Generate agent info"""
        return {
            "email": AGENT_TEST_EMAIL_ADDRESS,
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
            "username": "AlexAgent",
            "password": "randompassword123",
            "re_password": "randompassword123",
            "role": "AGT",
        }

    def generate_organizer_info(self) -> dict:
        """Generate organizer info"""

        return {
            "email": ORGANIZER_TEST_EMAIL_ADDRESS,
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
            "username": "AlexOrganizer",
            "password": "randompassword123",
            "re_password": "randompassword123",
            "role": "ORG",
        }

    def test_unauthorizated_create_agent(self):
        """Test for unauthorizated creation ofa single agent using API"""
        url = reverse("agents_app:agents-list")
        response = self.client.post(url, self.agent_info)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_forbidden_create_agent(self):
        """Test for forbidden creation of a single agent using API"""

        # Create and activatye an agent user
        url = reverse("customuser-list")
        response = self.client.post(url, self.agent_info)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        agent_user = User.objects.get(username=self.agent_info["username"])
        agent_user.is_active = True
        agent_user.save()

        # Login agent user and get token
        url = reverse("jwt-create")
        organizer_login_data = {
            "email": self.agent_info["email"],
            "password": self.agent_info["password"],
        }

        response = self.client.post(url, organizer_login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["access"])

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Agent creation
        url = reverse("agents_app:agents-list")
        response = self.client.post(url, self.agent_info)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_agent(self):
        """Test for creating a single agent using API"""

        # Create and activate an organizer user
        url = reverse("customuser-list")
        response = self.client.post(url, self.organizer_info)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        organizer_user = User.objects.get(username=self.organizer_info["username"])
        organizer_user.is_active = True
        organizer_user.save()

        # Login organizer user and get token
        url = reverse("jwt-create")
        organizer_login_data = {
            "email": self.organizer_info["email"],
            "password": self.organizer_info["password"],
        }

        response = self.client.post(url, organizer_login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["access"])

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Agent creation
        url = reverse("agents_app:agents-list")
        agent_info = {"user": self.agent_info}
        response = self.client.post(url, agent_info, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
