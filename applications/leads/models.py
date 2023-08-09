from django.db import models

from model_utils.models import TimeStampedModel

from applications.account.choices import GENDER_CHOICES
from applications.account.utils import set_age
from applications.agents.models import Agent


class Lead(TimeStampedModel):
    address = models.CharField("Address", max_length=100)
    phone = models.CharField("Phone number", max_length=50)
    last_name = models.CharField("Last name", max_length=50)
    first_name = models.CharField("First name", max_length=50)
    email = models.EmailField("Email", max_length=254, unique=True)
    birth = models.DateField("Birth", auto_now=False, auto_now_add=False)
    gender = models.CharField("Gender", choices=GENDER_CHOICES, max_length=10)

    agent = models.ForeignKey(
        Agent,
        on_delete=models.SET_NULL,
        null=True,
        related_name="leads",
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_age(self, birth):
        self.age = set_age(birth)

    def save(self, *args, **kwargs):
        self.age = set_age(self.birth)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
