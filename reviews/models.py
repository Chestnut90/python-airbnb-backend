from django.db import models

from commons.models import Common


class Review(Common):
    """Review model definition"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    # TODO : add experience
    comment = models.TextField()

    # TODO : validate input value from 0 to 5
    rating = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return f"{self.user} give {self.rating} to {self.room}"
