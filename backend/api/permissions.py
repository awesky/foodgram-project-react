from rest_framework import permissions


# ReDoc: Список рецептов - GET. Страница доступна всем пользователям
# ReDoc: Получение рецепта - GET, id
# ReDoc: Создание рецепта - POST. Доступно только авторизованному пользователю
# ReDoc: Обновление рецепта - PATCH, id. Доступно только автору данного рецепта
# ReDoc: Удаление рецепта - DELETE, id. Доступно только автору данного рецепта
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
