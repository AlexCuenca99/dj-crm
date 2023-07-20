from django.db import models
from django.contrib.auth import get_user_model

from model_utils.models import TimeStampedModel

from applications.account.models import UserProfile

User = get_user_model()


class Agent(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="agents")
    organization = models.ForeignKey(
        UserProfile, related_name="profiles", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.email
