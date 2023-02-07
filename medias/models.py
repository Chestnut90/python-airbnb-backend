from django.db import models

from commons.models import Common


class Photo(Common):
    """Photo model definition"""

    url = models.URLField()
    description = models.TextField()
    room = models.ForeignKey(
        "rooms.room",
        on_delete=models.CASCADE,
        related_name="photos",
    )

    def __str__(self) -> str:
        return f"photo of room{self.room.pk}"
