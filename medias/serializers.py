from rest_framework.serializers import ModelSerializer

from .models import Photo


class PhotoSerializer(ModelSerializer):
    class Meta:
        model = Photo
        exclude = [
            "created_at",
            "updated_at",
            "room",
        ]
