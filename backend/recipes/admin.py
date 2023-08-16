from django.contrib import admin

from . import models

# Вывод "пустого" значения.
EMPTY_VALUE: str = "-пусто-"


# REQ: Вывести все модели с возможностью редактирования и удаление записей.
class IngredientAdmin(admin.ModelAdmin):
    # REQ: В список вывести название ингредиента и единицы измерения.
    list_display = (
        "pk",
        "name",
        "measurement_unit",
    )
    search_fields = (
        "name",
        "measurement_unit",
    )
    # REQ: Администратор обладает всеми правами авторизованного пользователя
    # REQ: Плюс к этому он может:
    # REQ: - добавлять/удалять/редактировать ингредиенты.
    list_editable = (
        "name",
        "measurement_unit",
    )
    # REQ: Добавить фильтр по названию.
    list_filter = ("name",)
    empty_value_display = EMPTY_VALUE


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "color",
        "slug",
    )
    search_fields = (
        "name",
        "color",
        "slug",
    )
    # REQ: Администратор обладает всеми правами авторизованного пользователя
    # REQ: Плюс к этому он может:
    # REQ: - добавлять/удалять/редактировать теги.
    list_editable = (
        "name",
        "color",
        "slug",
    )
    list_filter = (
        "name",
        "color",
        "slug",
    )
    empty_value_display = EMPTY_VALUE


class RecipeAdmin(admin.ModelAdmin):
    # REQ: В списке рецептов вывести название и автора рецепта.
    list_display = (
        "pk",
        "name",
        "author",
        "image",
        "count_favorites",
    )
    # REQ: Администратор обладает всеми правами авторизованного пользователя
    # REQ: Плюс к этому он может:
    # REQ: - редактировать/удалять любые рецепты.
    list_editable = (
        "name",
        "author",
        "image",
    )
    # REQ: Добавить фильтры по автору, названию рецепта, тегам.
    list_filter = (
        "author",
        "name",
        "tags",
    )
    empty_value_display = EMPTY_VALUE

    # REQ: На странице рецепта вывести общее число добавлений
    # этого рецепта в избранное.
    def count_favorites(self, obj) -> int:
        # Связь с models.Favorite: related_name = 'favorites'.
        return obj.favorite.count()


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "recipe",
        "ingredient",
        "amount",
    )
    empty_value_display = EMPTY_VALUE


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "recipe",
    )
    search_fields = (
        "user",
        "recipe",
    )
    empty_value_display = EMPTY_VALUE


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "recipe",
    )
    search_fields = (
        "user",
        "recipe",
    )
    empty_value_display = EMPTY_VALUE


admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(models.Favorite, FavoriteAdmin)
admin.site.register(models.ShoppingCart, ShoppingCartAdmin)
