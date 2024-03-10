from rest_framework.decorators import action
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientFilter
from api.serializers import (TagSerializer,
                             RecipeSerializer,
                             IngredientSerializer)
from recipes.models import Tag, Recipe, Ingredient


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [IngredientFilter]
    search_fields = ["^name"]


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    @action(detail=False)
    def download_shopping_cart(self, request):
        return Response({"Hello": "Hello"})

    @action(detail=True,
            methods=["post", "delete"])
    def shopping_cart(self, request, pk=None):
        return Response({"Hello": "Hello"})

    @action(detail=True)
    def favorite(self, request, pk=None):
        return Response({"Hello": "Hello"})
