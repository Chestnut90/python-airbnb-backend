from rest_framework.serializers import ModelSerializer
from rooms.serializers import RoomSimpleSerializer
from .models import Wishlist


class WishlistSerializer(ModelSerializer):

    rooms = RoomSimpleSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )
