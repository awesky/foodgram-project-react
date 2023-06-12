"""
Модели для recipes.
"""
from django.core.validators import (
    MaxValueValidator, MinValueValidator, RegexValidator
)
from django.db import models

from users.models import CustomUser


User = CustomUser


class Ingredient(models.Model):
    """
    Модель ингридиента для Рецепта (Recipe).
    """
    # (string)
    name = models.CharField(
        'Название',
        max_length=200
    )
    # (string - из data/ingredients.json)
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Сортировка по-умолчанию
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Tag(models.Model):
    """
    Модель метки (тэга) для классификации Рецепта (Recipe).
    """
    # ReDoc: Название (string <= 200 characters).
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )
    # ReDoc: Цвет в HEX (string or null <= 7 characters).
    color = models.CharField(
        'Цветовой HEX-код',
        max_length=7,
        null=True,
        unique=True,
        # Валидация формата кода.
        validators=[
            RegexValidator(
                regex='^#([a-fA-F0-9]{6})',
                message='Неверный формат.'
            )
        ],
    )
    # ReDoc: Уникальный слаг
    # ReDoc: (string or null <= 200 characters ^[-a-zA-Z0-9_]+$).
    # Валидиция выполняется на уровне "SlugField"
    slug = models.SlugField(
        'Slug',
        max_length=200,
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']  # Сортировка по-умолчанию
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Recipe(models.Model):
    """
    Модель рецепта.
    """
    # ReDoc: Список ингредиентов (Array of objects).
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',
    )
    # ReDoc: Список id тегов (Array of integers).
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    # ReDoc: Картинка, закодированная в Base64 (string <binary>).
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True,
    )
    # ReDoc Название (string <= 200 characters).
    name = models.CharField(
        'Название',
        max_length=200,
    )
    # ReDoc: Описание (string)
    text = models.TextField(
        'Текстовое описание',
    )
    # ReDoc: Время приготовления (в минутах) (integer >= 1).
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                1, 'Не менее минуты!'
            )
        ]
    )
    # Автор рецепта
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']  # Сортировка по-умолчанию
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    """
    Модель количества Ингридиента (Ingredient) в Рецепте (Recipe).
    """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                1, 'Маловато будет!'
            ),
            MaxValueValidator(
                1000, 'Где ж взять столько?!'
            )
        ]
    )

    def __str__(self):
        return f'{self.recipe}: {self.ingredient}'

    class Meta:
        ordering = ['recipe']  # Сортировка по-умолчанию
        verbose_name = 'Ингредиенты в рецепте'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            ),
        )
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class Favorite(models.Model):
    """
    Модель отметки Пользователя (User) и избранного Рецепта (Recipe).
    """
    # Авторизованный пользователь
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET('Рецепт был удален.'),
        related_name='favorite',
    )
    
    class Meta:
        # Ограничение уникальности рецепта (Recipe)
        # в "Избранном" Пользователя (User).
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_recipe_user',
            ),
        )
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    """
    Модель Списка покупок ингридиентов (Ingradient(s)).
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipe',
    )

    class Meta:
        # Ограничение уникальности рецепта (Recipe)
        # в Списке покупок (ShoppingCart) Пользователя (User).
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart_recipe_user',
            ),
        )
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
