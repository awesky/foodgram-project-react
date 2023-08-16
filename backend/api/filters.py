from django_filters.rest_framework import filters, FilterSet

from recipes.models import Ingredient, Recipe, Tag, CustomUser


# ReDoc: Поиск по частичному вхождению в начале названия ингредиента
class IngredientFilter(FilterSet):
    """Фильтр для Ингредиента (Ingredient)."""
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )


# ReDoc: Доступна фильтрация по избранному, автору, списку покупок и тегам
class RecipeFilter(FilterSet):
    """Фильтр для Рецепта (Recipe)."""
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited')
    author = filters.ModelChoiceFilter(
        queryset=CustomUser.objects.all())
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', )

    # Определение метода для "is_favorited"
    def get_is_favorited(self, queryset, name, value):
        """Фильтр наличия в Избранном (Favorite)."""
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorite__user=user)
        return queryset

    # Определение метода для "is_in_shopping_cart"
    def get_is_in_shopping_cart(self, queryset, name, value):
        """Фильтр наличия в Спискe покупок (ShoppingCart)."""
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return queryset
