from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response

from api.serializers import FollowSerializer
from users.models import Follow
from users.paginations import LimitPagination
from users.serializers import CustomCreateUserSerializer, CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Отображение пользователей"""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = LimitPagination
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = CustomCreateUserSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        if self.action == "subscriptions":
            return User.objects.filter(following__user=self.request.user)
        return super().get_queryset()

    @action(detail=False, methods=["get"])
    def me(self, request):
        user = get_object_or_404(User, pk=self.request.user.id)
        serializer = CustomUserSerializer(user, context={"request": request})
        return Response(serializer.data)

    @action(detail=True,
            methods=["post"],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk):
        author = get_object_or_404(User, pk=pk)

        serializer = FollowSerializer(
            instance=author,
            data=request.data,
            context={"request": request})
        serializer.is_valid(raise_exception=True)
        Follow.objects.create(user=request.user, author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def subscribe_delete(self, request, pk):
        author = get_object_or_404(User, pk=pk)
        try:
            subscribe = Follow.objects.get(user=request.user, author=author)
        except ObjectDoesNotExist:
            raise ValidationError({"errors": "Таких подписок нет!"})
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        queryset = self.get_queryset()
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(pages, many=True,
                                      context={"request": request})
        return self.get_paginated_response(serializer.data)
