from api.views import IngredientViewSet, RecipeViewSet, TagViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"tags", TagViewSet)
router.register(r"recipes", RecipeViewSet, basename="Recipe")
router.register(r"ingredients", IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
