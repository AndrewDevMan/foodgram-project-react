from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator


User = get_user_model()


class DefaultRelatedNameModel(models.Model):
    """Абстрактная модель. Установка related_name."""

    class Meta:
        abstract = True
        default_related_name = "%(class)ss"


class Tag(models.Model):
    name = models.CharField('Название', max_length=32)
    slug = models.SlugField('Slug', unique=True, max_length=32)
    color = models.CharField(
        'Цвет в HEX',
        max_length=7,
        validators=[RegexValidator(
            regex=r'^#[A-Fa-f0-9]{6}$',
            message='Цвет надо указывать в HEX формате',
            code='Invalide color',
        )]
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=32)
    measurement_unit = models.CharField('Еденица измерения', max_length=32)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='recipe_images')
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    tags = models.ManyToManyField(Tag)
    time = models.IntegerField()

    class Meta(DefaultRelatedNameModel.Meta):
        pass

    def __str__(self):
        return self.title
