from datetime import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from ..utils import set_age


client = APIClient()
User = get_user_model()


class UserViewsetTest(APITestCase):
    """Test module for App Users API"""

    def setUp(self) -> None:
        self.user_data = {
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
        }

    def test_create_get_user(self):
        """Test module for CREATE a single user"""
        url = reverse("customuser-list")
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(id=response.data["id"])
        self.assertEqual(user.phone, self.user_data["phone"])
        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.gender, self.user_data["gender"])
        self.assertEqual(user.address, self.user_data["address"])
        self.assertEqual(user.username, self.user_data["username"])
        self.assertEqual(user.age, set_age(self.user_data["birth"]))
        self.assertEqual(user.last_name, self.user_data["last_name"])
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertTrue(user.password is not self.user_data["password"])
        self.assertTrue(user.is_staff is not True)
        self.assertTrue(user.is_admin is not True)
        self.assertTrue(user.is_active is not True)
        self.assertEqual(
            user.birth,
            datetime.strptime(self.user_data["birth"], "%Y-%m-%d").date(),
        )


class JWTTest(APITestCase):
    """Test case for LOGIN a user"""

    def setUp(self) -> None:
        self.user_data = {
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
        }

    def test_login_user(self):
        url_user = reverse("customuser-list")
        url_jwt = reverse("jwt-create")

        response = self.client.post(url_user, self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(id=response.data["id"])

        self.assertTrue(user.is_active is not True)

        user.is_active = True
        user.save()

        self.assertTrue(user.is_active is not False)

        response = self.client.post(
            url_jwt, {"email": user.email, "password": self.user_data["password"]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)

    def test_valid_token(self):
        url_user = reverse("customuser-list")
        url_jwt = reverse("jwt-create")
        url_verify = reverse("jwt-verify")

        response = self.client.post(url_user, self.user_data)
        user = User.objects.get(id=response.data["id"])

        user.is_active = True
        user.save()

        response = self.client.post(
            url_jwt, {"email": user.email, "password": self.user_data["password"]}
        )

        token = response.data["access"]

        response = self.client.post(url_verify, {"token": token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorized_user(self):
        url_user = reverse("customuser-list")
        url_jwt = reverse("jwt-create")
        url_users = reverse("customuser-list")

        response = self.client.post(url_user, self.user_data)
        user = User.objects.get(id=response.data["id"])
        user.is_active = True
        user.save()
        response = self.client.post(
            url_jwt, {"email": user.email, "password": self.user_data["password"]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data["access"]
        client.credentials(HTTP_AUTHORIZATION="JWT " + token)
        response = client.get(url_users)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
