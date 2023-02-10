from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """User Model Definition"""

    class GenderChoice(models.TextChoices):
        """Gender Choice class"""

        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    class LanguageChoice(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")

    class CurrencyChoice(models.TextChoices):
        WON = "won", "Korean Won"
        USD = "usd", "US Dollar"

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=150)

    gender = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        choices=GenderChoice.choices,
    )

    avatar = models.URLField(blank=True)

    language = models.CharField(
        max_length=2,
        choices=LanguageChoice.choices,
        blank=True,
    )
    currency = models.CharField(
        max_length=5,
        choices=CurrencyChoice.choices,
        blank=True,
    )

    is_host = models.BooleanField(default=False)

    # def is_host(self):
    #     return self.rooms.all().count() > 0
