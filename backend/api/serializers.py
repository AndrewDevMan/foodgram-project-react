from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingList, Tag)
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CharField, CurrentUserDefault,
                                        IntegerField, ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField)
from users.models import Follow
from users.serializers import CustomUserSerializer

User = get_user_model()


class Base64ImgField(Base64ImageField):
    """Поле для преобразрвания изображения"""

    def to_internal_value(self, base64_data):
        if base64_data in self.EMPTY_VALUES:
            raise ValidationError("Приложи фото рецепта")
        return super().to_internal_value(base64_data)


class IngredientSerializer(ModelSerializer):
    """Сериализатор для ингридиентов"""

    class Meta:
        model = Ingredient
        fields = "__all__"


class TagSerializer(ModelSerializer):
    """Сериализатор для тегов"""

    class Meta:
        model = Tag
        fields = ["id", "name", "color", "slug"]


class RecipeIngredientSerializer(ModelSerializer):
    """Сериализация ингредиентов в рецепте"""
    id = IntegerField(source="ingredient.id")
    name = CharField(source="ingredient.name")
    measurement_unit = CharField(source="ingredient.measurement_unit")

    class Meta:
        model = RecipeIngredient
        fields = ["id", "name", "measurement_unit", 'amount']


class RecipeReadSerializer(ModelSerializer):
    """Сериализация рецепта"""
    author = CustomUserSerializer(
        read_only=True,
        default=CurrentUserDefault(),
    )
    ingredients = RecipeIngredientSerializer(
        many=True,
        required=True,
        source="recipe"
    )
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImgField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ["id", "tags", "author", "ingredients", "is_favorited",
                  "is_in_shopping_cart", "name", "image", "text",
                  "cooking_time"]

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return (
            Favorite.objects
            .filter(recipe=obj, user=user).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return (
            ShoppingList.objects
            .filter(recipe=obj, user=user).exists()
        )


class IngredientsAddSerializer(ModelSerializer):
    """Сериализация ингридиента при создании рецепта"""
    id = IntegerField()
    amount = IntegerField()

    class Meta:
        model = Ingredient
        fields = ["id", "amount"]


class RecipeCreateSerializer(ModelSerializer):
    """Сериализация при создании рецепта"""
    ingredients = IngredientsAddSerializer(many=True)
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64ImgField()

    class Meta:
        model = Recipe
        fields = ["id", "tags", "author", "ingredients", "name", "image",
                  "text", "cooking_time"]
        read_only_fields = ["author"]

    @staticmethod
    def validate_ingredients(ingredients):
        if not ingredients:
            raise ValidationError("Добавьте хотябы один ингредиент")

        double_ingr = []
        for ingredient in ingredients:
            if int(ingredient.get("amount")) < 1:
                raise ValidationError(
                    "Колличество ингредиента не может быть меньше 1",
                )
            try:
                obj = Ingredient.objects.get(id=ingredient.get("id"))
            except ObjectDoesNotExist:
                raise ValidationError("Ингредиент не существует")
            if obj in double_ingr:
                raise ValidationError("Ингредиент не должен повторятся")
            else:
                double_ingr.append(obj)
        return ingredients

    @staticmethod
    def validate_tags(tags):
        if not tags:
            raise ValidationError("Добавьте хотябы один тег")

        double_tag = []
        for tag in tags:
            if tag in double_tag:
                raise ValidationError("Тег не должен повторятся")
            else:
                double_tag.append(tag)
        return tags

    @staticmethod
    def validate_cooking_time(cooking_time):
        if int(cooking_time) < 1:
            raise ValidationError(
                "Время приготовления не может быть меньше 1 мин"
            )
        return cooking_time

    def to_representation(self, instance):
        context = {"request": self.context.get("request")}
        return RecipeReadSerializer(instance, context=context).data

    @staticmethod
    def add_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get("id"),
                amount=ingredient.get("amount"),
            )

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.add_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        if "ingredients" not in validated_data:
            raise ValidationError("Добавьте хотябы один ингредиент")
        ingredients = validated_data.pop("ingredients")
        instance.ingredients.clear()
        self.add_ingredients(ingredients, instance)
        if "tags" not in validated_data:
            raise ValidationError("Добавьте хотябы один тег")
        instance.tags.set(validated_data.pop("tags"))
        return super().update(instance, validated_data)


class RecipeInFavoriteSerializer(ModelSerializer):
    """Сериализация для избранного и подписок"""
    image = Base64ImgField(read_only=True)

    class Meta:
        model = Recipe
        fields = ["id", "name", "image", "cooking_time"]
        read_only_fields = ["id", "name", "cooking_time"]


class FollowSerializer(ModelSerializer):
    """Сериализация для списка подписок"""
    is_subscribed = SerializerMethodField()
    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name",
                  "is_subscribed", "recipes", "recipes_count"]
        read_only_fields = ["email", "username", "first_name", "last_name"]

    def validate(self, attrs):
        user = self.context["request"].user
        author = self.instance
        if user == author:
            raise ValidationError(
                {"errors": "Не пытайтесь подписаться на себя!"}
            )
        if Follow.objects.filter(user=user, author=author).exists():
            raise ValidationError(
                {"errors": "Уже подписались!"}
            )
        return attrs

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        return Follow.objects.filter(user=user, author=obj).exists()

    @staticmethod
    def get_recipes_count(obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        recipes_limit: dict = {}
        try:
            recipes_limit = self.context["request"].GET["recipes_limit"]
        except KeyError:
            pass
        if recipes_limit:
            recipes = (Recipe.objects
                       .filter(author=obj)[:int(recipes_limit)])
        else:
            recipes = Recipe.objects.filter(author=obj)
        serializer = RecipeInFavoriteSerializer(recipes, many=True)
        return serializer.data
