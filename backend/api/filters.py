from django.contrib.auth import get_user_model
from django_filters.rest_framework.filters import (BooleanFilter,
                                                   ModelChoiceFilter,
                                                   ModelMultipleChoiceFilter)
from django_filters.rest_framework.filterset import FilterSet
from rest_framework.filters import SearchFilter

from recipes.models import Recipe, Tag

User = get_user_model()


class IngredientFilter(SearchFilter):
    """Фильтр для поска ингридиента"""
    search_param = "name"


class RecipeFilter(FilterSet):
    """Фильтр для поиска рецепта"""
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name="tags__slug",
        to_field_name="slug",
    )
    author = ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = BooleanFilter(method="filter_is_favorited")
    is_in_shopping_cart = BooleanFilter(method="filter_is_in_shopping_cart")

    class Meta:
        model = Recipe
        fields = ["tags", "author"]

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shoppinglists__user=user)
        return queryset
