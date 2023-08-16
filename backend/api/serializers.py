from django.shortcuts import get_object_or_404

from djoser.serializers import UserSerializer

from drf_extra_fields.fields import Base64ImageField

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    ImageField,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    SerializerMethodField,
)

from recipes.models import (
    Ingredient,
    Favorite,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
    Tag,
)
from users.models import CustomUser, Subscribtion


class CustomUserSerializer(UserSerializer):
    """ "
    Серилизатор модели Пользователя (CustomUser).
    """

    is_subscribed = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_subscribed",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "is_subscribed": {"read_only": True},
        }

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return None
        return Subscribtion.objects.filter(user=user, author=obj).exists()

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class SubscribtionRecipeListSerializer(ModelSerializer):
    """
    Вложенный сериализатор для SubscribtionSerializer.
    Обеспечивает обработку GET-запросов:
    формирование списка Рецептов (Recipes).
    """

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "cooking_time",
            "image",
        )


# ReDoc: Мои подписки - GET
# ReDoc: Подписаться на пользователя - POST, id
class SubscribtionSerializer(ModelSerializer):
    """
    Сериализатор модели Подписки (Subscribtion).
    Обеспечивает обработку GET и POST-запросов:
    обработка Подписки (Subscription) Пользователя (CustomUser).
    """

    email = ReadOnlyField(source="author.email")
    id = ReadOnlyField(source="author.id")
    username = ReadOnlyField(source="author.username")
    first_name = ReadOnlyField(source="author.first_name")
    last_name = ReadOnlyField(source="author.last_name")
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = Subscribtion
        fields = (
            # ReDoc: ("email", "id", "username",
            # "first_name", "last_name", "is_subscribed",
            # "recipes", "recipes_count")
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        """Возвращает значение существования Подписки (Subscription)."""
        return Subscribtion.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        """Возвращает Рецепты (Recipies) автора."""
        request = self.context.get("request")
        queryset = Recipe.objects.filter(author=obj.author)
        # ReDoc: Количество объектов внутри поля recipes
        limit = request.GET.get("recipes_limit")
        if limit:
            queryset = queryset[: int(limit)]
        return SubscribtionRecipeListSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        """Возвращает количество Рецептов (Recipies) автора."""
        return Recipe.objects.filter(author=obj.author).count()


# ReDoc: Список ингредиентов - GET
# ReDoc: Получение ингредиента - GET, id
class IngredientSerializer(ModelSerializer):
    """
    Сериализатор модели Ингредиент (Ingredient).
    Обеспечивает обработку GET запросов:
    чтение Ингридиента (Ingredient).
    """

    class Meta:
        model = Ingredient
        # ReDoc: "id", "name", "measurement_unit"
        fields = (
            "id",
            "name",
            "measurement_unit",
        )
        read_only_fields = fields


# ReDoc: Cписок тегов - GET
# ReDoc: Получение тега - GET, id
class TagSerializer(ModelSerializer):
    """
    Сериализатор модели Тег (Tag).
    Обеспечивает обработку GET запросов:
    чтение Тега (Tag).
    """

    class Meta:
        model = Tag
        # ReDoc: "id", "name", "color", "slug"
        fields = (
            "id",
            "name",
            "color",
            "slug",
        )
        read_only_fields = fields


class RecipeIngredientReadSerializer(ModelSerializer):
    """
    Вложенный сериализатор для RecipeReadSerialize.
    Обеспечивает чтение Ингридиента (Ingredient) из Рецепта (Recipe).
    """

    id = ReadOnlyField(source="ingredient.id")
    name = ReadOnlyField(source="ingredient.name")
    measurement_unit = ReadOnlyField(source="ingredient.measurement_unit")

    class Meta:
        model = RecipeIngredient
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )


# ReDoc: Список рецептов - GET
# ReDoc: Получение рецепта - GET, id
class RecipeReadSerializer(ModelSerializer):
    """
    Сериализатор чтения для модели Рецепта (Recipe).
    Обеспечивает обработку GET запросов.
    """

    # Проверить author после создания сериализатора для User
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientReadSerializer(
        many=True, read_only=True, source="recipe_ingredient"
    )
    tags = TagSerializer(many=True, read_only=True)
    # ReDoc: is_favorited (boolean)
    is_favorited = SerializerMethodField()
    # ReDoc: is_in_shopping_cart (boolean)
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        # ReDoc: ("id", "tags", "author", "ingredients",
        # "is_favorited", "is_in_shopping_cart",
        # "name", "image", "text", "cooking_time")
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = fields

    # Определение метода для "is_favorited"
    def get_is_favorited(self, obj):
        """Проверка наличия в Избранном (Favorite)."""
        request = self.context.get("request")
        return (
            request.user.is_authenticated
            and Favorite.objects.filter(user=request.user, recipe=obj).exists()
        )

    # Определение метода для "is_in_shopping_cart"
    def get_is_in_shopping_cart(self, obj):
        """Проверка наличия в Спискe покупок (ShoppingCart)."""
        request = self.context.get("request")
        return (
            request.user.is_authenticated
            and ShoppingCart.objects.filter(
                user=request.user, recipe=obj
            ).exists()
        )


class RecipeIngredientWriteSerializer(ModelSerializer):
    """
    Вложенный сериализатор для RecipeWriteSerializer.
    Обеспечивает работу с моделью связи
    Рецепта (Recipe) и Ингридиента (Ingredient)(RecipeIngredien).
    """

    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = (
            "id",
            "amount",
        )


# ReDoc: Создание рецепта - POST
# ReDoc: Обновление рецепта - PATCH, id
# ReDoc: Удаление рецепта - DELETE, id
class RecipeWriteSerializer(ModelSerializer):
    """
    Сериализатор записи (удаления) для модели Рецепта (Recipe).
    Обеспечивает обработку POST, PATCH и DELETE-запросов.
    """

    ingredients = RecipeIngredientWriteSerializer(many=True)
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            # ReDoc: ("ingredients", "tags", "image",
            # "name": "string", "text", "cooking_time")
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def validate_ingredients(self, value):
        """ "
        Валидирует назначение Ингредиентов (Ingredient) Рецепту (Recipes).
        """
        if not value:
            raise ValidationError(
                {"ingredients": "Рецепт не может быть без ингредиентов!"}
            )
        ingredients_list = []
        error_msg = ""
        for item in value:
            err = ""
            ingredient = get_object_or_404(Ingredient, name=item["id"])
            if ingredient in ingredients_list:
                err += f'Ингредиент "{ingredient.name}" повторяется.'
            error_msg += err
            ingredients_list.append(ingredient)
            if error_msg:
                raise ValidationError({"ingredients": error_msg})
        return value

    def validate_tags(self, value):
        """ "
        Валидирует назначение Тэгов (Tag) Рецепту (Recipes).
        """
        if not value:
            raise ValidationError({"tags": "Нужно указать хотя бы один тег!"})
        tags_list = []
        error_msg = ""
        for tag in value:
            err = ""
            if tag in tags_list:
                err += f"Тег {tag.name} повторяется!\n"
            error_msg += err
            tags_list.append(tag)
        if error_msg:
            raise ValidationError({"tags": error_msg})
        return value

    def take_ingredients_tags(self, recipe, ingredients, tags):
        """ "
        Создает связи между:
        Рецептом (Recipe) и Ингридиентами (Ingredient),
        Рецептом (Recipe) и Тегами (Tag).
        """
        for ingredient in ingredients:
            RecipeIngredient.objects.update_or_create(
                recipe=recipe,
                ingredient=ingredient["id"],
                amount=ingredient["amount"],
            )
        recipe.tags.set(tags)

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        recipe = Recipe.objects.create(
            author=self.context["request"].user,
            **validated_data,
        )
        self.take_ingredients_tags(
            recipe=recipe, ingredients=ingredients, tags=tags
        )
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        instance.ingredients.clear()
        instance.tags.clear()
        self.take_ingredients_tags(
            recipe=instance,
            ingredients=ingredients,
            tags=tags,
        )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(instance, context=self.context).data


# ReDoc: Добавить рецепт в избранное - POST, id
# ReDoc: Удалить рецепт из избранного - DELETE, id
class FavoriteSerializer(ModelSerializer):
    """Сериализатор модели Избранного (Favorite)."""

    id = PrimaryKeyRelatedField(source="recipe", read_only=True)
    name = ReadOnlyField(source="recipe.name")
    image = ImageField(source="recipe.image", read_only=True)
    cooking_time = IntegerField(source="recipe.cooking_time", read_only=True)

    class Meta:
        model = Favorite
        fields = (
            # ReDoc: "id", "name", "image", "cooking_time"
            "id",
            "name",
            "image",
            "cooking_time",
        )


# ReDoc: Добавить рецепт в список покупок - POST, id
# ReDoc: Удалить рецепт из списка покупок - DELETE, id
class ShoppingCartSerializer(ModelSerializer):
    """Сериализатор модели Списка покупок (ShoppingCart)."""

    id = PrimaryKeyRelatedField(source="recipe", read_only=True)
    name = ReadOnlyField(source="recipe.name")
    image = ImageField(source="recipe.image", read_only=True)
    cooking_time = IntegerField(source="recipe.cooking_time", read_only=True)

    class Meta:
        model = ShoppingCart
        fields = (
            # ReDoc: "id", "name", "image", "cooking_time"
            "id",
            "name",
            "image",
            "cooking_time",
        )
