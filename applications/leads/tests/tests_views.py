from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test.utils import override_settings

from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend", DEBUG=True
)
class GetAllLeadsTest(APITestCase):
    def setUp(self):
        """Set up a method which is used to initialize beofer any test run"""

        self.lead_info = self.generate_lead_info()
        self.agent_info = self.generate_agent_info()
        self.organizer_info = self.generate_organizer_info()
        self.assigned_lead_info = self.generate_assigned_lead_info()

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
            "agent": "",
        }

    def generate_assigned_lead_info(self) -> dict:
        """Generate lead info"""

        return {
            "address": "Example street",
            "phone": "123456789",
            "last_name": "Scott",
            "first_name": "Henry",
            "email": "henry-lead@crm.com",
            "birth": "1999-12-02",
            "gender": "M",
            "agent": 1,
        }

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
            "re_password": "randompassword123",
            "role": "AGT",
        }

    def generate_organizer_info(self) -> dict:
        """Generate organizer info"""

        return {
            "email": "alex-organizer@admin1.com",
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

    def test_unathorized_create_lead(self):
        """Test for creating a single lead using API"""
        url = reverse("leads_app:leads-list")
        response = self.client.post(url, self.lead_info)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_forbidden_create_lead(self):
        """
        Test for invalid creation of a single lead using API
        """

        # Agent user creation and activation
        url = reverse("customuser-list")
        response = self.client.post(url, self.agent_info)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        agent_user = User.objects.get(username=self.agent_info["username"])
        agent_user.is_active = True
        agent_user.save()

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

        # Lead creation
        url = reverse("leads_app:leads-list")
        response = self.client.post(url, self.lead_info)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lead(self):
        """
        Test for creating a single lead using API
        """

        # Organizer user creation and activation
        url = reverse("customuser-list")
        response = self.client.post(url, self.organizer_info)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        organizer_user = User.objects.get(username=self.organizer_info["username"])
        organizer_user.is_active = True
        organizer_user.save()

        # Login agent user and get token
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

        # Lead creation
        url = reverse("leads_app:leads-list")
        response = self.client.post(url, self.lead_info)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_assigned_lead(self):
        """
        Test for creating a single assigned lead using API
        """

        # Organizer user creation and activation
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

        # Agent user creation
        url = reverse("agents_app:agents-list")
        agent_info = {"user": self.agent_info}

        response = self.client.post(url, agent_info, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Lead creation
        url = reverse("leads_app:leads-list")
        response = self.client.post(url, self.assigned_lead_info)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
