from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from recipes import constants

User = get_user_model()


class BaseMetaModel(models.Model):
    """Абстрактная базовая модель"""

    class Meta:
        abstract = True
        ordering = ["-id"]
        default_related_name = "%(class)ss"


class Tag(models.Model):
    name = models.CharField(
        "Название",
        unique=True,
        max_length=constants.CHAR_LIMIT_TAG_NAME,
    )
    slug = models.SlugField(
        "Слаг",
        unique=True,
        max_length=constants.CHAR_LIMIT_TAG_SLUG_NAME,
    )
    color = models.CharField(
        "Цвет в HEX",
        help_text="Пример: #A7F300",
        max_length=constants.CHAR_LIMIT_TAG_HEX_COLOR,
        validators=[RegexValidator(
            regex=r"^#[A-Fa-f0-9]{6}$",
            message="Цвет надо указывать в HEX формате",
            code="Invalide color",
        )]
    )

    class Meta(BaseMetaModel.Meta):
        ordering = ["id"]
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name[:constants.VISUAL_CHAR]


class Ingredient(models.Model):
    name = models.CharField(
        "Название",
        max_length=constants.CHAR_LIMIT_INGREDIENT_NAME,
    )
    measurement_unit = models.CharField(
        "Еденица измерения",
        max_length=constants.CHAR_LIMIT_INGREDIENT_MEASUREMENT_UNIT,
    )

    class Meta(BaseMetaModel.Meta):
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return (f"{self.name[:constants.VISUAL_CHAR]},"
                f"{self.measurement_unit[:constants.VISUAL_CHAR]}")


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Автор",
    )
    name = models.CharField(
        "Название рецепта",
        max_length=constants.CHAR_LIMIT_RECIPE_NAME,
    )
    image = models.ImageField(
        "Изображение рецепта",
        upload_to="recipes/",
    )
    text = models.TextField("Инструкция по приготовлению")
    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        verbose_name="Ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="Тег",
        related_name="recipes"
    )
    cooking_time = models.PositiveSmallIntegerField(
        "Время готовки, мин.",
        validators=[MinValueValidator(
            limit_value=constants.MIN_VALUE_RECIPE_TIME_COOKING,
            message=f"Вы не можете указать меньше "
                    f"{constants.MIN_VALUE_RECIPE_TIME_COOKING} мин.",
        )]
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.name[:constants.VISUAL_CHAR]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингридиент",
        related_name="ingredient",
    )
    amount = models.PositiveSmallIntegerField(
        "Колличество",
        validators=[MinValueValidator(
            limit_value=constants.MIN_VALUE_RECIPEINGREDIENT_AMOUNT,
            message=f"Вы не можете указать меньше "
                    f"{constants.MIN_VALUE_RECIPEINGREDIENT_AMOUNT}.",
        )]
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецептах"

    def __str__(self):
        return (
            f"{self.ingredient.name[:constants.VISUAL_CHAR]} "
            f"{self.ingredient.measurement_unit[:constants.VISUAL_CHAR]} "
            f"- {self.amount}"
        )


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    class Meta(BaseMetaModel.Meta):
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"],
                name="unique_favorite",
            )]

    def __str__(self):
        return (f"{self.recipe[:constants.VISUAL_CHAR]} добавил в избранное "
                f"{self.user[:constants.VISUAL_CHAR]}")


class ShoppingList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    class Meta(BaseMetaModel.Meta):
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"],
                name="unique_shoppinglist",
            )]

    def __str__(self):
        return (f"{self.recipe[:constants.VISUAL_CHAR]} добавил в покупки "
                f"{self.user[:constants.VISUAL_CHAR]}")
