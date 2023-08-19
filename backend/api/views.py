from datetime import datetime

from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import CustomUser, Subscribtion

from .filters import IngredientFilter, RecipeFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeWriteSerializer,
                          ShoppingCartSerializer, SubscribtionSerializer,
                          TagSerializer)

# --- users app ---


class CustomUserViewSet(UserViewSet):
    """
    Viewset для Пользователя (CustomUser) и
    Подписок (Subscriptions) Пользователя (CustomUser).
    """

    @action(
        detail=False, permission_classes=(IsAuthenticated,), methods=["GET"]
    )
    # ReDoc: users/subscriptions/
    def subscriptions(self, request):
        """
        Возвращает пользователей, на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        """
        queryset = Subscribtion.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribtionSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        # ReDoc: Доступно только авторизованным пользователям
        permission_classes=(IsAuthenticated,),
        methods=["POST", "DELETE"],
    )
    # ReDoc: users/{id}/subscribe/
    def subscribe(self, request, id=None):
        """Подписывает / отписывает Пользователя от автора."""
        user = request.user
        author = get_object_or_404(CustomUser, id=id)
        # Котроль ограничения подписки на самого себя
        if user == author:
            message = (
                "Вы не можете подписаться " "на самого себя (или отписаться)."
            )
            return Response(
                {"errors": message}, status=status.HTTP_400_BAD_REQUEST
            )
        is_subscribed = Subscribtion.objects.filter(user=user, author=author)
        # Блок POST-запроса
        if self.request.method == "POST":
            if is_subscribed:
                return Response(
                    {
                        "errors": (
                            f"Вы уже подписаны на пользователя: "
                            f"{author.username}."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscribtion = Subscribtion.objects.create(
                user=user, author=author
            )
            serializer = SubscribtionSerializer(
                subscribtion, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Блок DELETE-запроса
        # Согласно ReDoc в случае некорректного запроса
        # требуется выдать ошибку 400 с описанием причины:
        # "Reoc: 400 Ошибка подписки (Например, если не был подписан)"
        # Чтобы отловить некорректный запрос, необходимо выполнить
        # проверку отсутствия подписки (в случае DELETE, ниже) и
        # проверку наличия подписки (в случае POST, выше)
        if is_subscribed:
            is_subscribed.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {
                "errors": (
                    f"Вы не подписаны на пользователя: " f"{author.username}."
                )
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


# --- recipes app ---


class IngredientViewSet(ReadOnlyModelViewSet):
    """ViewSet модели Ингредиент (Ingredient)."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    # ReDoc: Поиск по частичному вхождению в начале названия ингредиента
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    pagination_class = None


class TagViewSet(ReadOnlyModelViewSet):
    """ViewSet модели Тег (Tag)."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """ViewSet модели Рецепт (Recipe)."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    # ReDoc: Доступна фильтрация по избранному, автору, списку покупок и тегам
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    # Опрелеяем сериализатор в зависимости от типа запроса
    def get_serializer_class(self):
        # Блок GET-запроса
        if self.request.method == "GET":
            return RecipeReadSerializer
        # Блок POST/PATCH/DELETE-запроса
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        # ReDoc: Доступно только авторизованным пользователям
        permission_classes=(IsAuthenticated,),
    )
    # ReDoc: recipes/{id}/favorite/
    def favorite(self, request, *args, **kwargs):
        """Обработка Избранного (Favorite)."""
        recipe = get_object_or_404(Recipe, id=self.kwargs.get("pk"))
        user = request.user
        in_favorite = Favorite.objects.filter(recipe=recipe, user=user)
        # Блок POST-запроса
        if request.method == "POST":
            # Проверка наличия в Избранном
            if in_favorite:
                return Response(
                    # ReDoc: "errors": "string"
                    {"errors": "Рецепт был добавлен в Избранное ранее!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = FavoriteSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(recipe=recipe, user=user)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        # Блок DELETE-запроса
        if in_favorite:
            in_favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            # ReDoc: "errors": "string"
            {"errors": "Этого рецепта в Избранном нет!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=True,
        methods=["POST", "DELETE"],
        # ReDoc: Доступно только авторизованным пользователям
        permission_classes=(IsAuthenticated,),
        pagination_class=None,
    )
    # ReDoc: recipes/{id}/shopping_cart/
    def shopping_cart(self, request, **kwargs):
        """Обработка Списка покупок (ShoppingCart)."""
        recipe = get_object_or_404(Recipe, id=self.kwargs.get("pk"))
        in_shopping_cart = ShoppingCart.objects.filter(
            user=request.user, recipe=recipe
        )
        # Блок POST-запроса
        if request.method == "POST":
            if in_shopping_cart:
                return Response(
                    # ReDoc: "errors": "string"
                    {"errors": "Рецепт был добавлен в списке покупок ранее."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = ShoppingCartSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(recipe=recipe, user=request.user)
                return Response(
                    # 'Рецепт успешно удалён из списка покупок.',
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
        # Блок DELETE-запроса
        if in_shopping_cart:
            in_shopping_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            # ReDoc: "errors": "string"
            {"errors": "Этого рецепта в списке покупок нет."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        detail=False,
        methods=["GET"],
        # Доступно только авторизованным пользователям
        permission_classes=(IsAuthenticated,),
    )
    # recipes/download_shopping_cart/
    def download_shopping_cart(self, request):
        """Скачать Список покупок (ShoppingCart)."""
        ingredients = (
            ShoppingCart.objects.filter(user=request.user)
            .values(
                "recipe__ingredients__name",
                "recipe__ingredients__measurement_unit",
            )
            .annotate(amount=Sum("recipe__recipe_ingredient__amount"))
        )
        today = datetime.today()
        shopping_cart = (
            f"Список покупок от {today:%Y-%m-%d %H:%M}\n"
            f"Пользователь: {request.user.get_full_name()} "
            f"({request.user.username})\n"
        )
        for ingredient in ingredients:
            shopping_cart += (
                f'\n- {ingredient["recipe__ingredients__name"]}: '
                f'{ingredient["amount"]} '
                f'{ingredient["recipe__ingredients__measurement_unit"]}'
            )

        shopping_cart += "\n\nСформирован Продуктовым помощником Foodgram"

        filename = f"{today:%Y-%m-%d}_{request.user.username}_ShoppingCart.txt"
        response = HttpResponse(
            shopping_cart, content_type="text.txt; charset=utf-8"
        )
        response["Content-Disposition"] = f"attachment; filename={filename}"

        return response
