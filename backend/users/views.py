from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from djoser.views import UserViewSet

from users.models import Follow
from users.serializers import (UserSerializer, FollowSerializer,
                               CustomUserSerializer, CustomCreateUserSerializer)
from users.paginations import LimitPagination

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    pagination_class = LimitPagination

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = CustomCreateUserSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=False, methods=["get"])
    def me(self, request):
        user = get_object_or_404(User, pk=self.request.user.id)
        serializer = CustomUserSerializer(user, context={"request": request})
        return Response(serializer.data)
