from django.contrib import admin

from recipes.models import Ingredient, Tag, Recipe, RecipeIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "measurement_unit"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name", "slug"]


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ["author", "title"]
    list_display = ["author", "title"]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    search_fields = ["recipe", "ingredient"]
    list_display = ["recipe", "ingredient"]
