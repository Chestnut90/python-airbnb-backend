from statistics import mean

from django.db import models
from users.models import User

from commons.models import Common


class Amenity(Common):
    """Amenity Model Definition"""

    class Meta:
        verbose_name_plural = "Amenities"

    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Room(Common):

    """Room Model Definition"""

    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = ("entire_place", "Entire Place")
        PRIVATE_ROOM = ("private_room", "Private Room")
        SHARED_ROOM = ("shared_room", "Shared Room")

    name = models.CharField(max_length=140)

    country = models.CharField(
        max_length=50,
        #    default="Korea",
    )
    city = models.CharField(max_length=80)
    address = models.CharField(max_length=250)

    price = models.PositiveIntegerField()

    kind = models.CharField(max_length=20, choices=RoomKindChoices.choices)
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    amenities = models.ManyToManyField("rooms.Amenity", related_name="rooms")

    pet_friendly = models.BooleanField(default=True)

    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="rooms",
    )

    # reviews, categories ...

    def __str__(self) -> str:
        return self.name

    def total_amenities(self) -> int:
        return self.amenities.count()

    def get_rating(self):
        return round(
            0
            if self.reviews.count() == 0
            else mean([r.rating for r in self.reviews.all()]),
            1,
        )
