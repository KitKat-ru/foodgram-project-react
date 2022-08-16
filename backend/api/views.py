
from asyncore import read
from djoser.views import UserViewSet
from api.serializers import CustomUserSerializer, FavoriteSerializer
from .models import Favorite
from users.models import User
from ingredients.models import Ingredient, Tag
from recipes.models import Recipe
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from . import serializers # custom permissions
from django.shortcuts import get_object_or_404

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
    # serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.RecipeSerializer
        return serializers.RecipeCreateSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE',],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = FavoriteSerializer(data={'user': request.user.id, 'recipe': recipe.id})
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save(recipe=recipe, user=request.user)
            serializer = serializers.AbbreviatedRecipeSerializer(recipe)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            favorite = get_object_or_404(Favorite, user=request.user, recipe=recipe)
            favorite.delete()
            return Response('Рецепт удален', status=status.HTTP_204_NO_CONTENT)

