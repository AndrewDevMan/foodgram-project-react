# Generated by Django 4.2.10 on 2024-03-01 06:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_options_follow_follow_unique_user_author"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={
                "ordering": ["-id"],
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                max_length=150, unique=True, verbose_name="Имя пользователя"
            ),
        ),
    ]
