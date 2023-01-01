from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import User


class UserPrivateSerializer(ModelSerializer):
    is_host = SerializerMethodField()

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

    def get_is_host(self, user: User):
        return user.is_host()


class UserPublicSerialzier(ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "avatar")
