import rest_framework.permissions as rest_permissions
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from ingredients.models import Ingredient, Tag
from recipes.models import Recipe
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User

from . import permissions, serializers, filters, models



class CustomUserViewSet(UserViewSet):
    """Кастомный вьюсет от Dojser.
    Реализованы методы чтения, создания,
    частичного обновления и удаления объектов.
    """
    serializer_class = serializers.CustomUserSerializer
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
    queryset = Recipe.objects.all().order_by('-id')
    permission_classes = (
        rest_permissions.IsAuthenticatedOrReadOnly,
        permissions.AuthorOrReadOnly
    )
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.RecipeFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.RecipeSerializer
        return serializers.RecipeCreateSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE',],
        permission_classes=(IsAuthenticated,),
        url_name='favorite',
        url_path='favorite',
    )
    def favorite(self, request, pk):
        user=request.user
        data = {'user': user.id, 'recipe': pk}
        if request.method == 'POST':
            serializer = serializers.FavoriteSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        elif request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, pk=pk)
            favorite = models.Favorite.objects.filter(
                user=user.id, recipe=recipe
            )
            favorite.delete()
            return Response('Рецепт удален', status=status.HTTP_204_NO_CONTENT)
        return Response('Ошибка', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(
        detail=True,
        methods=['POST', 'DELETE',],
        permission_classes=(IsAuthenticated,),
        url_name='shopping_cart',
        url_path='shopping_cart',
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = serializers.ShoppingBasketSerializer(
            data={'user': request.user.id, 'recipe': recipe.id}
        )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save(recipe=recipe, user=request.user)
            serializer = serializers.AbbreviatedRecipeSerializer(recipe)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        elif request.method == 'DELETE':
            basket = get_object_or_404(
                models.ShoppingBasket, user=request.user, recipe=recipe
            )
            basket.delete()
            return Response('Рецепт удален', status=status.HTTP_204_NO_CONTENT)
        return Response('Ошибка', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
