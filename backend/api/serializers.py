import logging
from logging.handlers import RotatingFileHandler

from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from ingredients.models import Ingredient, Tag
from recipes.models import Favorite, Recipe, RecipeIngredient, ShoppingBasket
from users.models import Subscription, User

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'my_logger.log', maxBytes=50000000, backupCount=5
)
logger.addHandler(handler)


class AbbreviatedRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения и рецептов в избранном и корзине"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time', )
        read_only_fields = ('id', 'name', 'image', 'cooking_time', )


class CustomUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'is_subscribed',
        )


class CustomCreateUserSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя.
    Проверяет username на запрещенные значения.
    """
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name',
            'last_name', 'password',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username', )
            )
        ]

    def validate(self, attrs):
        """Проверка ввода недопустимого имени ("me") и уникальность полей."""
        if attrs['username'] == 'me':
            raise serializers.ValidationError(
                "Поле username не может быть 'me'."
            )
        if attrs['username'] == attrs['email']:
            raise serializers.ValidationError(
                'Поля email и username не должны совпадать.'
            )
        return attrs


class FavoriteSerializer(serializers.ModelSerializer):
    """Промежуточный сериализатор связи юзера-рецепта для избранного."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
    )

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message='Рецепт уже в избранном!',
            )
        ]

    def validate(self, attrs):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        recipe = attrs['recipe']
        if Favorite.objects.filter(
            user=request.user.id, recipe=recipe
        ).exists():
            raise serializers.ValidationError(
                {'status': 'Рецепт уже добавлен'}
            )
        return attrs

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return AbbreviatedRecipeSerializer(
            instance.recipe, context=context
        ).data


class SubscriptionListSerializer(CustomUserSerializer):
    """
    Сериализатор для представления списка подписок.
    Отнаследован от  CustomUserSerializer.
    """
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed',
    )
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes',
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count',
    )

    class Meta:
        model = Subscription
        fields = (
            'is_subscribed', 'recipes', 'recipes_count',
        )

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(
            user=obj.user, following=obj.following
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        paginate_qs = Recipe.objects.filter(author=obj.following)
        if limit:
            paginate_qs = paginate_qs[:int(limit)]
        return AbbreviatedRecipeSerializer(paginate_qs, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.following).count()


class ShoppingBasketSerializer(serializers.ModelSerializer):
    """Промежуточный сериализатор связи юзера-рецепта для корзины."""
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
    )

    class Meta:
        model = ShoppingBasket
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingBasket.objects.all(),
                fields=['user', 'recipe'],
                message='Рецепт уже в корзине!',
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return AbbreviatedRecipeSerializer(
            instance.recipe, context=context
        ).data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения и изменения данных о тегах."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug', )
        read_only_fields = ('id', 'name', 'color', 'slug', )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения данных об ингридиентах."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Промежуточный сериализатор для связи ингридиентов-рецепта-количества."""
    id = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='id',
        # Выгружаем все ингредиенты через поле ingridient в
        # промежуточной таблице RecipeIngredient и берем все объекты
        # ингридиентов связанные в промежуточной модели
        queryset=Ingredient.objects.all()
    )
    name = serializers.SlugRelatedField(
        # Ссылаемся на модель Ingredient и берем название
        source='ingredient',
        slug_field='name',
        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        # Ссылаемся на модель Ingredient и берем единицу измерения
        source='ingredient',
        slug_field='measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        # Указываем подтянутые из Ingredient поля и добавляем поле amount
        fields = ('id', 'name', 'measurement_unit', 'amount', )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения и изменения данных об ингридиентах."""
    # Вложенный сериализатор
    author = CustomUserSerializer(read_only=True)
    # В get_ingredients создаем qs связанных ингредиентов с рецептом. Данные
    # беруться из промежуточной таблицы RecipeIngredients, пполученный qs
    # отдаем в сериализатор для "отображения" которое нужно нам
    ingredients = serializers.SerializerMethodField()
    # Вложенный сериализатор, список
    tags = TagSerializer(many=True, read_only=True)
    # Кастомное поле для предобразования байтовой строки в картинку
    image = Base64ImageField()
    # Кастомное поле в котором провверяется булево наличия в промежуточной
    # таблицы Favorite
    is_favorited = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_favorited',
    )
    # Кастомное поле в котором провверяется булево наличия в промежуточной
    # таблицы ShoppingBasket
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients', 'tags', 'name', 'image',
            'text', 'cooking_time', 'is_favorited', 'is_in_shopping_cart'
        )

    def get_ingredients(self, obj):
        queryset = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(queryset, many=True).data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Favorite.objects.filter(
                user=user, recipe=obj
            ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return ShoppingBasket.objects.filter(
                user=user, recipe=obj
            ).exists()
        return False


class CreateIngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления в recipe данных об ингридиентах."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount', )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения recipe."""
    author = CustomUserSerializer(read_only=True)
    ingredients = CreateIngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
        )

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data

    def validate(self, attrs):
        logger.info(attrs)
        if not attrs['ingredients'] or not attrs['tags']:
            raise serializers.ValidationError(
                'Добавьте ингредиенты и укажите тег для рецепта!'
            )
        ingredients = attrs['ingredients']
        min_ingredients = 2
        if len(ingredients) < min_ingredients:
            raise serializers.ValidationError(
                'Ингредиентов должно быть два или больше!'
            )
        data = []
        for ingredient in ingredients:
            logger.info(ingredient['amount'])
            data.append(ingredient['id'])
            if ingredient['amount'] <= 0:
                ingredient_incorrect = ingredient['id']
                logger.info(ingredient['amount'])
                raise serializers.ValidationError(
                    f'ЕИ - ингредиента "{ingredient_incorrect}" не'
                    'должна быть равна нулю или отрицательным числом!'
                )
        logger.info(data)
        check_unique = set(data)
        if len(check_unique) != len(data):
            raise serializers.ValidationError(
                'Ингридиенты должны быть уникальны!'
            )
        if attrs['cooking_time'] <= 0:
            raise serializers.ValidationError(
                'Время приготовления должно быть больше нуля!'
            )
        return attrs

    @staticmethod
    def adding_ingredients(ingredients, obj):
        bulk_list = [
            RecipeIngredient(
                recipe_id=obj.id,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        return RecipeIngredient.objects.bulk_create(bulk_list)

    @staticmethod
    def adding_tags(tags, obj):
        return obj.tags.set(tags)

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.adding_tags(tags=tags, obj=recipe)
        self.adding_ingredients(ingredients=ingredients, obj=recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self.adding_tags(tags=tags, obj=instance)
        self.adding_ingredients(ingredients=ingredients, obj=instance)
        return super().update(instance, validated_data)
