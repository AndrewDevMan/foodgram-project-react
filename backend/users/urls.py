from django.urls import path, include
from rest_framework import routers

from users.views import CustomUserViewSet

router = routers.DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="User")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
]
