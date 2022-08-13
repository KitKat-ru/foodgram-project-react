from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField
from rest_framework.validators import UniqueTogetherValidator

from users.models import User
from ingredients.models import Ingredient, Tag
from recipes.models import Recipe, RecipeIngredient, RecipeTag


import logging
from logging.handlers import RotatingFileHandler


# logging.basicConfig(
#     level=logging.DEBUG,
#     filename='main.log',
#     filemode='w'
# )
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = RotatingFileHandler('my_logger.log', maxBytes=50000000, backupCount=5)
logger.addHandler(handler)


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
    # logger.info(f'{id.source}')
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

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time',) # 'is_favorited', 'is_in_shopping_cart'

    def get_ingredients(self, obj):
        queryset = RecipeIngredient.objects.filter(recipe=obj)
        return RecipeIngredientSerializer(queryset, many=True).data


class CreateIngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления в recipe данных об ингридиентах."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount' )


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и изменения recipe."""
    logger.info(f'Я внутри сериализатора')
    author = CustomUserSerializer(read_only=True)
    ingredients = CreateIngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image', 'text', 'cooking_time',)

    def create(self, validated_data):
        logger.info(f'{self}')
        logger.info(f'rer')
        logger.info(f'{validated_data}')
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=author, **validated_data)
        for tag in tags:
            recipe.tags.add(tag)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient=ingredient['id'], recipe=recipe, amount=ingredient['amount'])
        return recipe
    
    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data

    def update(self, instance, validated_data):
        logger.info(f'{self.data}')
        logger.info(f'Я тут')
        logger.info(f'{validated_data}')
        logger.info(f'Я тут')
        # logger.info(f'{instance.context}')
        instance.tags.clear()
        RecipeIngredient.objects.filter(recipe=instance).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        for tag in tags:
            instance.tags.add(tag)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient=ingredient['id'], recipe=instance, amount=ingredient['amount'])
        return super().update(instance, validated_data)