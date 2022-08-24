import logging
from logging.handlers import RotatingFileHandler

from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from ingredients.models import Ingredient, Tag
from recipes.models import Recipe, RecipeIngredient
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.models import User

from .models import Favorite, ShoppingBasket, Subscription

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('my_logger.log', maxBytes=50000000, backupCount=5)
logger.addHandler(handler)


class AbbreviatedRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения и рецептов в избранном и корзине"""
    # image = Base64ImageField()

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
            raise serializers.ValidationError({'status': 'Рецепт уже добавлен'})
        return attrs

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return AbbreviatedRecipeSerializer(instance.recipe, context=context).data


class SubscriptionListSerializer(serializers.ModelSerializer):
    """Сериализатор для представления списка подписок."""
    id = serializers.ReadOnlyField(source='following.id')
    email = serializers.ReadOnlyField(source='following.email')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
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
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count', 
        )

        def get_is_subscribed(self, obj):
            return Subscription.objects.filter(
                user=obj.user, following=obj.following
            ).exists()
        
        def recipes(self, obj):
            request = self.context.get('request')
            limit = request.GET.get('recipes_limit')
            qs = Recipe.objects.filter(author=obj.following)
            if limit:
                paginate_qs = qs[:int(limit)]
            return AbbreviatedRecipeSerializer(qs, many=True).data

        def recipes_count(self, obj):
            return Recipe.objects.filter(author=obj.following).count





class ShoppingBasketSerializer(serializers.ModelSerializer):
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
        return AbbreviatedRecipeSerializer(instance.recipe, context=context).data


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
        # read_only=True
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
    # Через MethodField вызываем метод get_ingredients в котором ищем все
    # ingredient связанные с recipe в промежуточной таблице и передаем в
    # сериализатор как qset
    ingredients = serializers.SerializerMethodField()
    # Вложенный сериализатор
    tags = TagSerializer(many=True, read_only=True)
    # Кастомное поле для предобразования байтовой строки в картинку
    image=Base64ImageField()
    is_favorited = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_favorited',
    )
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
    # logger.info(f'Я внутри сериализатора')
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

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient=ingredient['id'],
                recipe=recipe,
                amount=ingredient['amount'])
        return recipe
    
    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data

    def update(self, instance, validated_data):
        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        for tag in tags:
            instance.tags.add(tag)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient=ingredient['id'],
                recipe=instance,
                amount=ingredient['amount'])
        return super().update(instance, validated_data)