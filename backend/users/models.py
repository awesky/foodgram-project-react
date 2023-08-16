"""
Foodgram user models.
"""
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """
    Модель Пользователя (CustomUser).
    """

    # ReDoc: Адрес электронной почты (string <email> <= 254 characters)
    # REQ: Email
    email = models.EmailField(
        "Электронная почта",
        max_length=254,
        unique=True,
        blank=False,
        null=False,
    )
    # ReDoc: Уникальный юзернейм (string <= 150 characters ^[\w.@+-]+\z)
    # REQ: Логин
    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=[
            # Проверка на допустимые символы
            RegexValidator(
                regex=r"^[\w.@+-]+$",
                message="Допустимые символы: буквы, цифры и @/./+/-/_",
            )
        ],
    )
    # ReDoc: Имя (string <= 150 characters)
    # REQ: Имя
    first_name = models.CharField(
        "Имя",
        max_length=150,
        blank=False,
        null=False,
    )
    # ReDoc: Фамилия (string <= 150 characters)
    # REQ: Фамилия
    last_name = models.CharField(
        "Фамилия", max_length=150, blank=False, null=False
    )
    # ReDoc: Пароль (string <= 150 characters)
    # REQ: Пароль
    password = models.CharField(
        "Пароль",
        max_length=150,
        blank=False,
        null=False,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        "username",
        "first_name",
        "last_name",
        "password",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Subscribtion(models.Model):
    """
    Модель подписки на автора Рецепта (Recipe.author).
    """

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user",
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="author",
    )

    class Meta:
        # Ограничение уникальности подписки на автора
        # для Пользователя (CustomUser)
        constraints = [
            models.UniqueConstraint(
                fields=("user", "author"),
                name="unique_user_author",
            )
        ]
        verbose_name = "Подписка на авторов"
        verbose_name_plural = "Подписка на авторов"
