from django.db import models
from commons.models import Common


class Wishlist(Common):
    """Wishlist Model definition"""

    name = models.CharField(
        max_length=150,
    )
    rooms = models.ManyToManyField(
        "rooms.Room",
        related_name="wish_rooms",
    )
    user = models.ForeignKey(
        "users.user",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return self.name
