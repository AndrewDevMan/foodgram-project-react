from api.views import TagViewSet, RecipeViewSet, IngredientViewSet
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"tags", TagViewSet)
router.register(r"recipes", RecipeViewSet, basename="Recipe")
router.register(r"ingredients", IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
