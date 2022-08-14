from djoser.views import UserViewSet
from api.serializers import CustomUserSerializer
from users.models import User
from ingredients.models import Ingredient, Tag
from recipes.models import Recipe, RecipeIngredient, RecipeTag
from rest_framework import (filters, generics, mixins, response, status,
                            viewsets)
from . import serializers # custom permissions


class CustomUserViewSet(UserViewSet):
    """Кастомный вьюсет от Dojser.
    Реализованы методы чтения, создания,
    частичного обновления и удаления объектов.
    """
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет Ингридиенты.
    Реализованы методы чтения списка объектов и отдельного объекта.
    """
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет Теги.
    Реализованы методы чтения списка объектов и отдельного объекта.
    """
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет Рецептов.
    Реализованы методы чтения списка объектов и создания нового рецепта.
    Чтение, изменение и удаление отдельного объекта.
    """
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.RecipeSerializer
        return serializers.RecipeCreateSerializer
    

    