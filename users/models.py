from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """user"""

    class GenderChoice(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    name = models.CharField(max_length=150)
    gender = models.CharField(
        max_length=10,
        choices=GenderChoice.choices,
    )
