import base64

from django.core.files.base import ContentFile
from rest_framework.serializers import ModelSerializer, ImageField

from recipes.models import Ingredient, Tag, Recipe


class IngredientSerializer(ModelSerializer):
    """Сериализатор для ингридиентов"""
    class Meta:
        model = Ingredient
        fields = "__all__"


class TagSerializer(ModelSerializer):
    """Сериализатор для тегов"""
    class Meta:
        model = Tag
        fields = "__all__"


class Base64ImgField(ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            frmt, imgstr = data.split(';base64,')
            ext = frmt.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(ModelSerializer):
    ingredient = IngredientSerializer()
    tag = TagSerializer()
    image = Base64ImgField()

    class Meta:
        model = Recipe
        fields = "__all__"
