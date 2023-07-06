from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", max_length=254, unique=True)
    username = models.CharField("Username", max_length=100, unique=True)
    first_name = models.CharField("First name", max_length=100)
    last_name = models.CharField("Last name", max_length=100)
    phone = models.CharField("Phone number", max_length=50)
    address = models.CharField("Address", max_length=100)
    birth = models.DateField("Birth", auto_now=False, auto_now_add=False)
    age = models.PositiveSmallIntegerField("Age")
    photo = models.ImageField(
        "Profile photo",
        upload_to=None,
        height_field=None,
        width_field=None,
        max_length=None,
    )
    is_active = models.BooleanField("Is active?", default=False)
    is_staff = models.BooleanField("Is staff member?", default=False)
    is_admin = models.BooleanField("Is admin?", default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "birth",
        "address",
        "phone",
    ]

    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email
