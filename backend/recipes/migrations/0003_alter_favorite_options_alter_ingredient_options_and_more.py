# Generated by Django 4.2.10 on 2024-03-01 06:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0002_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="favorite",
            options={
                "default_related_name": "%(class)ss",
                "ordering": ["-id"],
                "verbose_name": "Избранное",
                "verbose_name_plural": "Избранное",
            },
        ),
        migrations.AlterModelOptions(
            name="ingredient",
            options={
                "default_related_name": "%(class)ss",
                "ordering": ["-id"],
                "verbose_name": "Ингридиент",
                "verbose_name_plural": "Ингридиенты",
            },
        ),
        migrations.AlterModelOptions(
            name="recipeingredient",
            options={
                "default_related_name": "%(class)ss",
                "ordering": ["-id"],
                "verbose_name": "Ингредиент в рецепте",
                "verbose_name_plural": "Ингредиенты в рецептах",
            },
        ),
        migrations.AlterModelOptions(
            name="shoppinglist",
            options={
                "default_related_name": "%(class)ss",
                "ordering": ["-id"],
                "verbose_name": "Избранное",
                "verbose_name_plural": "Избранное",
            },
        ),
        migrations.AlterModelOptions(
            name="tag",
            options={
                "default_related_name": "%(class)ss",
                "ordering": ["-id"],
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
            },
        ),
    ]
