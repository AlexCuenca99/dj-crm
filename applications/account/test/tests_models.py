from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import logging

from ..models import CustomUser

from ..utils import set_age, photo_file_name


class CreateSingleUserTest(TestCase):
    def setUp(self) -> None:
        image = SimpleUploadedFile(
            "test_image.png", b"dummy_content", content_type="image/jpeg"
        )

        self.super_user_data = {
            "email": "admin@admin.com",
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "is_staff": True,
            "is_admin": True,
            "is_active": True,
            "phone": "0989181061",
            "gender": "M",
            "photo": image,
        }

        self.user_data = {
            "email": "admin@admin.com",
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
            "photo": image,
        }

        self.user_data_no_image = {
            "email": "admin@admin.com",
            "birth": "1999-12-02",
            "first_name": "Alex",
            "last_name": "Cuenca",
            "address": "Fausto Molina",
            "phone": "0989181061",
            "gender": "F",
        }

    def test_create_superuser(self):
        superuser = CustomUser.objects.create(**self.super_user_data)

        self.assertEqual(superuser.email, self.super_user_data["email"])
        self.assertEqual(superuser.phone, self.super_user_data["phone"])
        self.assertEqual(superuser.birth, self.super_user_data["birth"])
        self.assertEqual(superuser.age, set_age(self.user_data["birth"]))
        self.assertEqual(superuser.gender, self.super_user_data["gender"])
        self.assertEqual(superuser.address, self.super_user_data["address"])
        self.assertEqual(superuser.is_staff, self.super_user_data["is_staff"])
        self.assertEqual(superuser.is_admin, self.super_user_data["is_admin"])
        self.assertEqual(superuser.last_name, self.super_user_data["last_name"])
        self.assertEqual(superuser.is_active, self.super_user_data["is_active"])
        self.assertEqual(superuser.first_name, self.super_user_data["first_name"])
        self.assertEqual(
            superuser.photo.name,
            photo_file_name(superuser, filename=self.user_data["photo"].name),
        )

    def test_create_user(self):
        user = CustomUser.objects.create(**self.user_data)

        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.gender, self.user_data["gender"])
        self.assertEqual(user.phone, self.user_data["phone"])
        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.birth, self.user_data["birth"])
        self.assertEqual(user.address, self.user_data["address"])
        self.assertEqual(user.age, set_age(self.user_data["birth"]))
        self.assertEqual(user.last_name, self.user_data["last_name"])
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(
            str(user.photo.name),
            photo_file_name(user, filename=self.user_data["photo"].name),
        )

    def test_create_user_no_image(self):
        user = CustomUser.objects.create(**self.user_data)

        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.gender, self.user_data["gender"])
        self.assertEqual(user.phone, self.user_data["phone"])
        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.birth, self.user_data["birth"])
        self.assertEqual(user.address, self.user_data["address"])
        self.assertEqual(user.age, set_age(self.user_data["birth"]))
        self.assertEqual(user.last_name, self.user_data["last_name"])
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(
            str(user.photo.name),
            photo_file_name(user, "no-user-photo.png"),
        )
