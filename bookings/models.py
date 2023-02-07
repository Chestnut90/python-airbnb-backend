from django.db import models
from commons.models import Common


class Booking(Common):
    """Booking definition"""

    # how to handle this booking when after deletion user or room
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    room = models.ForeignKey(
        "rooms.Room",
        null=True,
        on_delete=models.SET_NULL,
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return f"booking for {self.user}"
