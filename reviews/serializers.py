from rest_framework.serializers import ModelSerializer

from .models import Review

from users.serializers import UserPublicSerialzier


class ReviewSerializer(ModelSerializer):
    """Review Model serializer"""

    user = UserPublicSerialzier(read_only=True)

    class Meta:
        model = Review
        exclude = ("id",)
