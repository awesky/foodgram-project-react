from django.contrib import admin

from . import models


# Вывод "пустого" значения.
EMPTY_VALUE: str = '-пусто-'


# REQ: Вывести все модели с возможностью редактирования и удаление записей.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'username', 'email', 'password', 'first_name', 'last_name',
    )
    # REQ: Администратор обладает всеми правами авторизованного пользователя
    # REQ: Плюс к этому он может:
    # REQ: - изменять пароль любого пользователя
    list_editable = ('password',)
    # REQ: Добавить фильтр списка по email и имени пользователя
    list_filter = ('email', 'username')
    search_fields = ('pk', 'username', 'email', 'first_name', 'last_name',)
    empty_value_display = EMPTY_VALUE


class FollowerUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'follower', 'author')
    list_editable = ('follower', 'author')
    empty_value_display = EMPTY_VALUE


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.FollowerUser, FollowerUserAdmin)
