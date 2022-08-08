from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from users.models import User
from ingredients.models import Ingredient, Tag
from recipes.models import Recipe, RecipeIngredient, RecipeTag


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.BooleanField(read_only=True)
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


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения и изменения данных о тегах."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения и изменения данных об ингридиентах."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Промежуточный сериализатор для связи ингридиентов-рецепта-количества."""
    id = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='id',
        # read_only=True
        # Выгружаем все ингредиенты и берем ID связанных с recipe
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
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения и изменения данных об ингридиентах."""
    # Вложенные сериализатор
    author = CustomUserSerializer()
    # Через MethodField вызываем метод get_ingredients в котором ищем все
    # ингредиенты связанные с recipe и передаем в промежуточный сериализатор
    # как qset 
    ingredients = serializers.SerializerMethodField(read_only=True)
    # Вложенный сериализатор
    tags = TagSerializer(many=True)
    # Кастомное поле для предобразования байтовой строки в картинку
    image=Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'description', 'cooking_time',) # 'is_favorited', 'is_in_shopping_cart'

    def get_ingredients(self, obj):
        queryset = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(queryset, many=True).data
