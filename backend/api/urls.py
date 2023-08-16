"""
api URL Configuration
"""
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from . import views

# ReDoc: '/api/'
app_name = 'api'

# Определение роутера api
router_api = DefaultRouter()
# ReDoc: 'users/'
router_api.register(
    # ReDoc: Мои подписки - GET
    # ReDoc: Подписаться на пользователя - POST, id
    # ReDoc: Отписаться от пользователя - DELETE, id
    'users', views.CustomUserViewSet, basename='users'
)
# ReDoc: 'tags/'
router_api.register(
    # ReDoc: Cписок тегов - GET
    # ReDoc: Получение тега - GET, id
    'tags', views.TagViewSet, basename='tags'
)
# ReDoc: 'ingredients/'
router_api.register(
    # ReDoc: Список ингредиентов - GET
    # ReDoc: Получение ингредиента - GET, id
    'ingredients', views.IngredientViewSet, basename='ingredients'
)
# ReDoc: 'recipes/'
router_api.register(
    # ReDoc: Список рецептов - GET
    # ReDoc: Получение рецепта - GET, id
    # ReDoc: Создание рецепта - POST
    # ReDoc: Обновление рецепта - PATCH, id
    # ReDoc: Удаление рецепта - DELETE, id
    # ReDoc: Добавить рецепт в избранное - POST, id
    # ReDoc: Удалить рецепт из избранного - DELETE, id
    # ReDoc: Добавить рецепт в список покупок - POST, id
    # ReDoc: Удалить рецепт из списка покупок - DELETE, id
    # ReDoc: Скачать список покупок - GET
    'recipes', views.RecipeViewSet, basename='recipes'
)

urlpatterns = [
    # api
    path('', include(router_api.urls)),
    # Djoser
    # https://djoser.readthedocs.io/en/latest/authentication_backends.html
    path('', include('djoser.urls')),
    re_path(r'auth/', include('djoser.urls.authtoken')),
]
