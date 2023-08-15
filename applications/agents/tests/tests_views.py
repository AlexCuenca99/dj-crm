ORGANIZER_TEST_EMAIL_ADDRESS = "alex@alex.com"
AGENT_TEST_EMAIL_ADDRESS = "mafoh16227@touchend.com"

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
import json

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Agent
from ..serializers import AgentModelSerializer
from applications.leads.models import Lead

User = get_user_model()


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


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend", DEBUG=True
)
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


class EditSingleAssignedLeadTest(APITestCase):
    def setUp(self) -> None:
        """Set up a method which is used to initialize before any test run"""
        self.agent_info = self.generate_agent_info()
        self.agent2_info = self.generate_agent2_info()
        self.lead_info = self.generate_lead_info()
        self.valid_payload = self.generate_valid_payload()

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
            # "re_password": "randompassword123",
            "role": "AGT",
        }

    def generate_agent2_info(self) -> dict:
        """Generate agent 2 info"""
        return {
            "email": "agent@agent2.com",
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
            "username": "AlexAgent2",
            "password": "randompassword123",
            # "re_password": "randompassword123",
            "role": "AGT",
        }

    def generate_lead_info(self) -> dict:
        """Generate lead info"""
        return {
            "address": "Example street",
            "phone": "123456789",
            "last_name": "Scott",
            "first_name": "Henry",
            "email": "henry-lead@crm.com",
            "birth": "1999-12-02",
            "gender": "M",
        }

    def generate_valid_payload(self) -> dict:
        """Generate valid payload"""
        return {"category": "ASG"}

    def test_forbidden_update_lead_assigned_me(self):
        """Test for creating a single lead assigned by me using API"""

        # User 2 and agent 2 creation
        user = User.objects.create_user(**self.agent2_info)
        user.is_active = True
        user.save()

        organization = user.user_profile
        self.assertEquals(organization.id, 1)
        agent_user = Agent.objects.create(user=user, organization=organization)
        self.assertEquals(agent_user.id, 1)

        # User creation
        user = User.objects.create_user(**self.agent_info)
        user.is_active = True
        user.save()
        organization = user.user_profile

        self.assertEquals(organization.id, 2)

        # Agent creation
        agent_user = Agent.objects.create(user=user, organization=organization)
        self.assertEquals(agent_user.id, 2)

        # Lead creation
        lead = Lead.objects.create(**self.lead_info)
        lead.agent = agent_user
        lead.save()

        self.assertEquals(lead.agent.id, 2)

        # Login agent user and get token
        url = reverse("jwt-create")
        agent_login_data = {
            "email": self.agent2_info["email"],
            "password": self.agent2_info["password"],
        }
        response = self.client.post(url, agent_login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["access"])

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Category Update
        url = reverse("agents_app:agents-my-leads", kwargs={"lead_pk": lead.id})

        response = self.client.patch(
            url,
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_lead_assigned_me(self):
        """Test for creating a single lead assigned by me using API"""

        # User creation
        user = User.objects.create_user(**self.agent_info)
        user.is_active = True
        user.save()
        organization = user.user_profile

        self.assertEquals(organization.id, 1)

        # Agent creation
        agent_user = Agent.objects.create(user=user, organization=organization)
        self.assertEquals(agent_user.id, 1)

        # Lead creation
        lead = Lead.objects.create(**self.lead_info)
        lead.agent = agent_user
        lead.save()

        self.assertEquals(lead.agent.id, 1)

        # Login agent user and get token
        url = reverse("jwt-create")
        agent_login_data = {
            "email": self.agent_info["email"],
            "password": self.agent_info["password"],
        }
        response = self.client.post(url, agent_login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["access"])

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Category Update
        url = reverse("agents_app:agents-my-leads", kwargs={"lead_pk": lead.id})

        response = self.client.patch(
            url,
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllAssignedAgentLeadsTest(APITestCase):
    def setUp(self) -> None:
        self.agent_info = self.generate_agent_info()
        self.lead_info = self.generate_lead_info()

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
            # "re_password": "randompassword123",
            "role": "AGT",
        }

    def generate_lead_info(self) -> dict:
        """Generate lead info"""
        return {
            "address": "Example street",
            "phone": "123456789",
            "last_name": "Scott",
            "first_name": "Henry",
            "email": "henry-lead@crm.com",
            "birth": "1999-12-02",
            "gender": "M",
        }

    def test_get_all_assigned_agent_leads(self):
        """Test for get all leads assigned to an agent"""

        # User creation
        user = User.objects.create_user(**self.agent_info)
        user.is_active = True
        user.save()
        organization = user.user_profile

        self.assertEquals(organization.id, 1)

        # Agent creation
        agent_user = Agent.objects.create(user=user, organization=organization)
        self.assertEquals(agent_user.id, 1)

        # Lead creation
        lead = Lead.objects.create(**self.lead_info)
        lead.agent = agent_user
        lead.save()

        self.assertEquals(lead.agent.id, 1)

        # Login agent user and get token
        url = reverse("jwt-create")
        agent_login_data = {
            "email": self.agent_info["email"],
            "password": self.agent_info["password"],
        }
        response = self.client.post(url, agent_login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["access"])

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Get all leads assigned to agent
        url = reverse("agents_app:agents-all-my-leads")
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
