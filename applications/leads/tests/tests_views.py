from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Lead

User = get_user_model()


class GetAllLeadsTest(APITestCase):
    def setUp(self):
        """Set up a method which is used to initialize beofer any test run"""

        self.lead_info = self.generate_lead_info()
        self.agent_info = self.generate_agent_info()
        self.organizer_info = self.generate_organizer_info()

    def generate_lead_info(self) -> dict:
        """Generate lead info"""

        return {
            "address": "Example street",
            "phone": "123456789",
            "last_name": "Scott",
            "first_name": "Henry",
            "email": "henry@crm.com",
            "birth": "1999-12-02",
            "gender": "M",
            "agent": "",
        }

    def generate_agent_info(self) -> dict:
        """Generate agent info"""

        return {
            "email": "admin1@admin1.com",
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
            "username": "AdminAdmin",
            "password": "randompassword123",
            "re_password": "randompassword123",
            "role": "AGT",
        }

    def generate_organizer_info(self) -> dict:
        """Generate organizer info"""

        return {
            "email": "admin1@admin1.com",
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
            "username": "AdminAdmin",
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
            "email": "admin1@admin1.com",
            "password": "randompassword123",
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

        agent_user = User.objects.get(username=self.agent_info["username"])
        agent_user.is_active = True
        agent_user.save()

        # Login agent user and get token
        url = reverse("jwt-create")
        agent_login_data = {
            "email": "admin1@admin1.com",
            "password": "randompassword123",
        }
        response = self.client.post(url, agent_login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["access"])

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Lead creation
        url = reverse("leads_app:leads-list")
        response = self.client.post(url, self.lead_info)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
