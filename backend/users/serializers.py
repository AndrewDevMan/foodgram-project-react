from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework.serializers import SerializerMethodField
from users.models import Follow

User = get_user_model()


class CustomCreateUserSerializer(UserSerializer):
    """Сериализация для создания пользователя"""
    class Meta:
        model = User
        fields = ["email", "id", "username", "first_name", "last_name",
                  "password"]
        extra_kwargs = {"password": {"write_only": True}}


class CustomUserSerializer(UserSerializer):
    """Сериализация для отображения пользователя/лей"""
    is_subscribed = SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj).exists()

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name",
                  "is_subscribed"]
