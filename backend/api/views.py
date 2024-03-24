from datetime import datetime as dt

from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Sum
from django.shortcuts import HttpResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.views import Response, status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import IngredientFilter, RecipeFilter
from api.paginations import LimitPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (IngredientSerializer, RecipeCreateSerializer,
                             RecipeInFavoriteSerializer, RecipeReadSerializer,
                             TagSerializer)
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Отображение ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [IngredientFilter]
    search_fields = ["^name"]


class TagViewSet(ReadOnlyModelViewSet):
    """Отображение тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """Отображение рецептов"""
    queryset = Recipe.objects.all()
    permission_classes = [AuthorOrReadOnly]
    filterset_class = RecipeFilter
    pagination_class = LimitPagination
    lookup_field = "pk"

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def add(model, request, pk):
        """Функция для добавления в избранное или корзину"""
        obj = model.objects.filter(user=request.user, recipe__pk=pk)
        if obj.exists():
            return Response({"errors": "Рецепт уже был добавлен!"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            recipe = Recipe.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise ValidationError({"errors": "Рецепт не найден!"})
        serializer = RecipeInFavoriteSerializer(
            instance=recipe,
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        model.objects.create(user=request.user, recipe=recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def dalete(model, request, pk):
        """Функция для удаления из избранного или корзины"""
        obj = model.objects.filter(user=request.user, recipe__pk=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"errors": "Рецепт уже был удалён!"},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=["post", "delete"],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        if request.method == "POST":
            return self.add(Favorite, request, pk)
        if request.method == "DELETE":
            return self.dalete(Favorite, request, pk)

    @action(detail=True,
            methods=["post", "delete"],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        if request.method == "POST":
            return self.add(ShoppingList, request, pk)
        if request.method == "DELETE":
            return self.dalete(ShoppingList, request, pk)

    @action(detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Подготовка файла со списком покупок"""
        user = request.user
        if not user.shoppinglists.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        clear_ingredients = {}
        ingredients = RecipeIngredient.objects.filter(
            recipe__shoppinglists__user=user.id
        ).values(
            "ingredient__name",
            "ingredient__measurement_unit"
        ).annotate(amount=Sum("amount"))

        for ingredient in ingredients:
            if ingredient["ingredient__name"] not in clear_ingredients:
                clear_ingredients[ingredient["ingredient__name"]] = {
                    "unit": ingredient["ingredient__measurement_unit"],
                    "amount": ingredient["amount"],
                }
            else:
                clear_ingredients[ingredient["ingredient__name"]]["amount"] +=\
                    ingredient["amount"]

        today = dt.today()
        shoplist = f"Список покупок на {today:%d %B %Y}\n\n"
        shoplist += "\n".join(
            [f"- {name} --- {clear_ingredients[name]['amount']}, "
             f"{clear_ingredients[name]['unit']}"
             for name in clear_ingredients]
        )

        file = f'shopping_list_{today:%d%m%y}.txt'
        response = HttpResponse(shoplist, content_type="text/plain")
        response["Content-Disposition"] = f"attachment; filename={file}"

        return response
