from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from core.constants import Limit


class User(AbstractUser):
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]
    USERNAME_FIELD = "email"

    username = models.CharField(
        "Имя пользователя",
        max_length=Limit.CHAR_LIMIT_USER_USERNAME,
        blank=False,
        unique=True,
        validators=[RegexValidator(
            regex=r"^[\w.@+-]+\Z",
            message="Можно использовать буквы латинского алфавита, цифры и "
                    "символы: '.', '@', '_', '-', '+'.",
            code="Invalide username",
        )]
    )
    email = models.EmailField(
        "Эл. почта",
        max_length=Limit.CHAR_LIMIT_USER_EMAIL,
        blank=False,
        unique=True,
    )
    first_name = models.CharField(
        "Имя",
        max_length=Limit.CHAR_LIMIT_USER_FIRST_NAME,
        blank=False,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=Limit.CHAR_LIMIT_USER_LAST_NAME,
        blank=False,
    )
    password = models.CharField(
        "Пароль",
        max_length=Limit.CHAR_LIMIT_USER_PASSWORD,
        blank=False,
    )

    class Meta:
        ordering = ["-id"]
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
