from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    REQUIRED_FIELDS = [
        "email",
        "first_name",
        "last_name",
    ]

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
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Follow(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        constraints = [models.UniqueConstraint(
                fields=["user", "author"],
                name="unique_user_author",
            )]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
