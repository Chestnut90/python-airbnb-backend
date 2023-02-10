from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import User


class UserPrivateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "name",
            "email",
            "gender",
            "is_host",
            "language",
            "currency",
            "avatar",
        )


class UserPublicSerialzier(ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "avatar")
