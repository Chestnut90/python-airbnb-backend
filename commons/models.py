from django.db import models
from django.contrib.auth.models import AbstractUser


class Common(models.Model):
    """Common Model Definition"""

    class Meta:
        abstract = True  # do not create table.

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # auto_now_add(add value when data created), auto_now(update value when it modified)
