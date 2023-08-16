"""
Модели для recipes.
"""
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models

from users.models import CustomUser

# Определяем пользователя
USER = CustomUser


class Ingredient(models.Model):
    """
    Модель Ингридиента для Рецепта (Recipe).
    """

    # REQ: Все поля обязательны для заполнения
    # ReDoc: (string)
    # REQ: Название
    name = models.CharField(verbose_name="Название", max_length=200)
    # ReDoc: (string - из data/ingredients.json)
    # REQ: Единицы измерения
    measurement_unit = models.CharField(
        verbose_name="Единица измерения",
        max_length=200,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"


class Tag(models.Model):
    """
    Модель Тэга (метки) для классификации Рецепта (Recipe).
    """

    # REQ: Все поля обязательны для заполнения и уникальны
    # ReDoc: Название (string <= 200 characters)
    # REQ: Название
    name = models.CharField(
        verbose_name="Название",
        max_length=200,
        unique=True,
    )
    # ReDoc: Цвет в HEX (string or null <= 7 characters)
    # REQ: Цветовой HEX-код (например, #49B64E)
    color = models.CharField(
        verbose_name="Цветовой HEX-код",
        max_length=7,
        null=True,
        unique=True,
        # Валидация формата кода.
        validators=[
            RegexValidator(
                regex="^#([a-fA-F0-9]{6})", message="Неверный формат HEX-кода."
            )
        ],
    )
    # ReDoc: Уникальный слаг
    # ReDoc: (string or null <= 200 characters ^[-a-zA-Z0-9_]+$).
    # REQ: Slug
    # Валидиция выполняется на уровне "SlugField"
    slug = models.SlugField(
        verbose_name="Slug",
        max_length=200,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class Recipe(models.Model):
    """
    Модель рецепта.
    """

    # ReDoc: Список id тегов (Array of integers)
    # REQ: Тег (можно установить несколько тегов на один рецепт,
    # REQ: выбор из предустановленных).
    tags = models.ManyToManyField(
        Tag,
        related_name="recipe",
        verbose_name="Теги",
    )
    # REQ: Автор публикации
    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="recipe",
        verbose_name="Автор",
    )
    # REQ: Все поля обязательны для заполнения.
    # ReDoc: Список ингредиентов (Array of objects)
    # REQ: Ингредиенты: продукты для приготовления блюда по рецепту:
    # множественное поле, выбор из предустановленного списка,
    # с указанием количества и единицы измерения
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="recipe",
        through="RecipeIngredient",
        # through_fields=('recipe', 'ingredient'),
        verbose_name="Ингредиенты",
    )
    # ReDoc: Название (string <= 200 characters)
    # REQ: Название
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    # ReDoc: Картинка, закодированная в Base64 (string <binary>)
    # REQ: Картинка
    image = models.ImageField(
        blank=True,
        upload_to="recipes/img/",
        verbose_name="Картинка",
    )
    # ReDoc: Описание (string)
    # REQ: Текстовое описание
    text = models.TextField(
        verbose_name="Текстовое описание",
    )
    # ReDoc: Время приготовления (в минутах) (integer >= 1)
    # REQ: Время приготовления в минутах
    cooking_time = models.PositiveSmallIntegerField(
        # ReDoc: Время приготовления (в минутах) (integer >= 1)
        verbose_name="Время приготовления",
        validators=[MinValueValidator(1, "Не менее минуты!")],
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"


class RecipeIngredient(models.Model):
    """
    Модель связи Рецепта (Recipe) и Ингридиента (Ingredient).
    """

    # REQ: Все поля обязательны для заполнения
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="recipe_ingredient",
        verbose_name="Рецепт",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.SET("Ингредиент был удален."),
        related_name="recipe_ingredient",
        verbose_name="Ингредиент",
    )
    # REQ: Количество
    amount = models.PositiveSmallIntegerField(
        "Количество", validators=[MaxValueValidator(1000)]
    )

    def __str__(self):
        return f"{self.recipe}: {self.amount} {self.ingredient}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]
        ordering = ["recipe"]
        verbose_name = "Ингредиенты в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"


class Favorite(models.Model):
    """
    Модель Избранного (Рецепт (Recipe) для Пользователя (User)).
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET("Рецепт был удален."),
        related_name="favorite",
    )
    user = models.ForeignKey(
        USER, on_delete=models.CASCADE, related_name="favorite"
    )

    class Meta:
        # Ограничение уникальности рецепта (Recipe)
        # в Избранном Пользователя (User).
        constraints = [
            models.UniqueConstraint(
                fields=("recipe", "user"),
                name="unique_favorite",
            )
        ]
        ordering = ["id"]
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"


class ShoppingCart(models.Model):
    """
    Модель Списка покупок Ингридиентов (Ingredient).
    """

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
    )
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
    )

    class Meta:
        # Ограничение уникальности рецепта (Recipe)
        # в Списке покупок (ShoppingCart) Пользователя (User).
        constraints = [
            models.UniqueConstraint(
                fields=("user", "recipe"),
                name="unique_shopping_cart",
            )
        ]
        ordering = ["user"]
        verbose_name = "Список покупок"
        verbose_name_plural = "Списки покупок"
