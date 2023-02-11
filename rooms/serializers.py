from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Amenity, Room

from users.serializers import UserPublicSerialzier
from medias.serializers import PhotoSerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "pk",
            "name",
            "description",
        )


class RoomSerializer(ModelSerializer):
    # connect other serializer into existed fields.
    owner = UserPublicSerialzier(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)
    photos = PhotoSerializer(many=True, read_only=True)
    rating = SerializerMethodField()

    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.get_rating()


class RoomSimpleSerializer(ModelSerializer):

    rating = SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "pk",
            "name",
            "address",
            "city",
            "country",
            "price",
            "rating",
            "photos",
            # like, photos
        )

    def get_rating(self, room):
        return room.get_rating()
