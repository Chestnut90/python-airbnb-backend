from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Amenity, Room

from users.serializers import UserPublicSerialzier


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("name", "description")


class RoomSerializer(ModelSerializer):
    # connect other serializer into existed fields.
    owner = UserPublicSerialzier(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = "__all__"


class RoomSimpleSerializer(ModelSerializer):

    rating = SerializerMethodField()

    class Meta:
        model = Room
        fields = (
            "name",
            "address",
            "city",
            "country",
            "price",
            "rating",
            # like, photos
        )

    def get_rating(self, room):
        return room.get_rating()
