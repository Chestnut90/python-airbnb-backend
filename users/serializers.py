from rest_framework.serializers import ModelSerializer

from .models import User


class UserPrivateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            # "password",
            "email",
            "gender",
        )


class UserPublicSerialzier(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")
