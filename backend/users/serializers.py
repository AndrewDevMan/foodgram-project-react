from django.contrib.auth import get_user_model
from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        PrimaryKeyRelatedField)

from users.models import Follow
from djoser.serializers import UserSerializer

User = get_user_model()


class CustomCreateUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ["email", "id", "username", "first_name", "last_name",
                  "password"]
        extra_kwargs = {'password': {'write_only': True}}


class CustomUserSerializer(UserSerializer):

    is_subscribed = SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()

    class Meta:
        model = User
        fields = ["email", "id", "username", "first_name", "last_name",
                  "is_subscribed"]


class FollowSerializer(ModelSerializer):

    user = PrimaryKeyRelatedField(read_only=True)
    author = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Follow
        fields = "__all__"
