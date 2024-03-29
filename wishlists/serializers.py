from rest_framework.serializers import ModelSerializer

from .models import Wishlist

from rooms.serializers import RoomSimpleSerializer


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
