from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from core.constants import Limit

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
        max_length=Limit.CHAR_LIMIT_TAG_NAME,
    )
    slug = models.SlugField(
        "Слаг",
        unique=True,
        max_length=Limit.CHAR_LIMIT_TAG_SLUG_NAME,
    )
    color = models.CharField(
        "Цвет в HEX",
        help_text="Пример: #A7F300",
        max_length=Limit.CHAR_LIMIT_TAG_HEX_COLOR,
        validators=[RegexValidator(
            regex=r"^#[A-Fa-f0-9]{6}$",
            message="Цвет надо указывать в HEX формате",
            code="Invalide color",
        )]
    )

    class Meta(BaseMetaModel.Meta):
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        "Название",
        max_length=Limit.CHAR_LIMIT_INGREDIENT_NAME,
    )
    measurement_unit = models.CharField(
        "Еденица измерения",
        max_length=Limit.CHAR_LIMIT_INGREDIENT_MEASUREMENT_UNIT,
    )

    class Meta(BaseMetaModel.Meta):
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Автор",
    )
    title = models.CharField(
        "Название рецепта",
        max_length=Limit.CHAR_LIMIT_RECIPE_TITLE,
    )
    image = models.ImageField(
        upload_to="recipe_images",
    )
    text = models.TextField("Описание")
    ingredient = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        verbose_name="Ингридиенты",
    )
    tag = models.ManyToManyField(
        Tag,
        verbose_name="Тег",
    )
    time = models.PositiveSmallIntegerField(
        "Время готовки, мин.",
        validators=[MinValueValidator(
            limit_value=Limit.MIN_VALUE_RECIPE_TIME_COOKING,
            message=f"Вы не можете указать меньше "
                    f"{Limit.MIN_VALUE_RECIPE_TIME_COOKING} мин.",
        )]
    )

    class Meta(BaseMetaModel.Meta):
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингридиент",
    )
    amount = models.PositiveSmallIntegerField(
        "Колличество",
        validators=[MinValueValidator(
            limit_value=Limit.MIN_VALUE_RECIPEINGREDIENT_AMOUNT,
            message=f"Вы не можете указать меньше "
                    f"{Limit.MIN_VALUE_RECIPEINGREDIENT_AMOUNT}.",
        )]
    )

    class Meta(BaseMetaModel.Meta):
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецептах"

    def __str__(self):
        return (
            f"{self.ingredient.name} "
            f"{self.ingredient.measurement_unit} - {self.amount}"
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
        return f"{self.recipe} добавил в избранное {self.user}"


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
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "user"],
                name="unique_shoppinglist",
            )]

    def __str__(self):
        return f"{self.recipe} добавил в избранное {self.user}"
