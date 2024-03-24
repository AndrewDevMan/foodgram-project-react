from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)

admin.site.empty_value_display = "---"


class RecipeIngredientInline(admin.TabularInline):
    """Инлайн для RecipeIngredient"""
    model = RecipeIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Админка для Ingredient"""
    search_fields = ["name"]
    list_display = ["id", "name", "measurement_unit"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Админка для Tag"""
    list_display = ["name", "slug", "color"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка для Recipe"""
    list_filter = ["author", "name", "tags"]
    list_display = ["author", "name", "id", "in_favorites"]
    readonly_fields = ["in_favorites"]
    inlines = [RecipeIngredientInline]
    filter_horizontal = ["tags"]

    @admin.display(description="В избранных, раз")
    def in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Админка для RecipeIngredient"""
    list_display = ["recipe", "ingredient", "amount"]


@admin.register(ShoppingList)
class ShoppingCartAdmin(admin.ModelAdmin):
    """Админка для ShoppingList"""
    list_display = ["user", "recipe"]


@admin.register(Favorite)
class FavouriteAdmin(admin.ModelAdmin):
    """Админка для Favorite"""
    list_display = ["user", "recipe"]
