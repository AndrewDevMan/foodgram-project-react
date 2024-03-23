from django.urls import include, path
from rest_framework import routers

from api.views import IngredientViewSet, RecipeViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r"tags", TagViewSet)
router.register(r"recipes", RecipeViewSet, basename="Recipe")
router.register(r"ingredients", IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
