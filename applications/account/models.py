import uuid
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from model_utils.models import TimeStampedModel

from .choices import GENDER_CHOICES, ROLE_CHOICES
from .utils import set_age, photo_file_name
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    age = models.PositiveSmallIntegerField("Age")
    address = models.CharField("Address", max_length=100)
    phone = models.CharField("Phone number", max_length=50)
    last_name = models.CharField("Last name", max_length=100)
    is_admin = models.BooleanField("Is admin?", default=False)
    first_name = models.CharField("First name", max_length=100)
    is_active = models.BooleanField("Is active?", default=False)
    email = models.EmailField("Email", max_length=254, unique=True)
    is_staff = models.BooleanField("Is staff member?", default=False)
    role = models.CharField("Role", choices=ROLE_CHOICES, max_length=50)
    username = models.CharField("Username", max_length=100, unique=True)
    birth = models.DateField("Birth", auto_now=False, auto_now_add=False)
    gender = models.CharField("Gender", choices=GENDER_CHOICES, max_length=10)
    photo = models.ImageField(
        "Profile photo",
        upload_to=photo_file_name,
        height_field=None,
        width_field=None,
        max_length=None,
        default="accounts/images/photos/no-user-photo.png",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
        "birth",
        "address",
        "phone",
        "gender",
    ]

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} - {self.last_name}"

    def set_age(self, birth):
        self.age = set_age(birth)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        self.age = set_age(self.birth)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(
        "CustomUser", related_name="user_profile", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.user.email


# Signal for new UserProfile instance creation only when a user is created
def post_user_created_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=CustomUser)
