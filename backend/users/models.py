from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = models.SlugField(
        "Имя пользователя",
        max_length=150,
        blank=False,
        unique=True,
    )
    email = models.EmailField(
        "Эл. почта",
        max_length=254,
        blank=False,
        unique=True,
    )
    first_name = models.CharField(
        "Имя",
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=150,
        blank=False,
    )
    password = models.CharField(
        "Пароль",
        max_length=150,
        blank=False,
    )

    class Meta:
        ordering = ["username"]

    def __str__(self):
        return self.username
