from django.contrib.auth import get_user_model

from djoser.serializers import UserCreatePasswordRetypeSerializer, UserSerializer

User = get_user_model()


class UserCreatePasswordRetypeCustomSerializer(UserCreatePasswordRetypeSerializer):
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + ("role", "password", "email")


class UserCustomSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            ("id",)
            + tuple(User.REQUIRED_FIELDS)
            + ("email", "role", "age", "is_active", "is_staff", "photo")
        )
