from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers

from users.models import User
from ingredients.models import Ingredient, Tag
from recipes.models import Recipe, RecipeIngredient, RecipeTag


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
        )


class CustomCreateUserSerializer(UserCreateSerializer):
    """Сериализатор создания пользователя.
    Проверяет username на запрещенные значения.
    """
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name', 'password',
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
