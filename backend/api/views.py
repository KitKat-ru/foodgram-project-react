import rest_framework.permissions as rest_permissions
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjUserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ingredients.models import Ingredient, Tag
from recipes.models import Favorite, Recipe, ShoppingBasket
from users.models import Subscription, User

from . import filters, pagination, permissions, serializers, services


class CustomUserViewSet(DjUserViewSet):
    """Кастомный вьюсет от Dojser.
    Реализованы методы чтения, создания,
    частичного обновления и удаления объектов.
    Добавлены эндпоинты для подписки/отписки от автора рецепта.
    Добавлен эндпоинт просмотра подписок.
    """
    serializer_class = serializers.CustomUserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='subscribe',
        url_name='subscribe',
        permission_classes=(IsAuthenticated, )
    )
    def subscribe(self, request, id):
        """Эндпоинт для подписки на автора или удаления из списка подписок."""
        user = request.user
        following = get_object_or_404(User, id=id)
        chain_follow = Subscription.objects.filter(
            user=user.id, following=following.id
        )
        if request.method == 'POST':
            if user == following:
                return Response(
                    {'errors': 'Нельзя подписаться на самого себя'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if chain_follow.exists():
                return Response(
                    {'errors': 'Вы уже подписаны на этого автора'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscribe = Subscription.objects.create(
                user=user,
                following=following
            )
            subscribe.save()
            serializer = serializers.SubscriptionListSerializer(
                subscribe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            chain_follow.delete()
            return Response('Отписка', status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'errors': 'Вы уже отписались'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        methods=['GET'],
        url_path='subscriptions',
        url_name='subscriptions',
        permission_classes=(IsAuthenticated, )
    )
    def subscriptions(self, requset):
        """Эндпоинт для фильтрации 'Подписок'."""
        user = requset.user
        qs = Subscription.objects.filter(user=user)
        if qs:
            pages = self.paginate_queryset(qs)
            serializer = serializers.SubscriptionListSerializer(
                pages,
                many=True,
                context={'request': requset},
            )
            return self.get_paginated_response(serializer.data)
        return Response(
            {'error': 'У Вас еще нет подписок'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет Ингридиенты.
    Реализованы методы чтения списка объектов и отдельного объекта.
    """
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    pagination_class = None
    permission_classes = (rest_permissions.AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = filters.SearchIngredientFilter
    search_fields = ('^name', )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет Теги.
    Реализованы методы чтения списка объектов и отдельного объекта.
    """
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (rest_permissions.AllowAny, )


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
    filter_backends = (DjangoFilterBackend, )
    filterset_class = filters.RecipeFilter
    pagination_class = pagination.CustomPagination

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.RecipeSerializer
        return serializers.RecipeCreateSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,),
        url_name='favorite',
        url_path='favorite',
    )
    def favorite(self, request, pk):
        """Эндпоинт для фильтрации 'Избранного'."""
        user = request.user
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
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, pk=pk)
            favorite = Favorite.objects.filter(
                user=user.id, recipe=recipe
            )
            favorite.delete()
            return Response('Рецепт удален', status=status.HTTP_204_NO_CONTENT)
        return Response('Ошибка', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,),
        url_name='shopping_cart',
        url_path='shopping_cart',
    )
    def shopping_cart(self, request, pk):
        """Эндпоинт для формирования списка покупок в корзине."""
        user = request.user
        data = {'user': user.id, 'recipe': pk}
        if request.method == 'POST':
            serializer = serializers.ShoppingBasketSerializer(
                data=data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, pk=pk)
            basket = ShoppingBasket.objects.filter(
                user=user.id, recipe=recipe
            )
            basket.delete()
            return Response('Рецепт удален', status=status.HTTP_204_NO_CONTENT)
        return Response('Ошибка', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,),
        url_name='download_shopping_cart',
        url_path='download_shopping_cart',
    )
    def download_shopping_cart(self, request):
        """Эндпоинт для скачивания списка покупок из корзины."""
        user = request.user
        basket = serializers.ShoppingBasket.objects.filter(user=user)
        if not basket:
            return Response('Корзина путса!')
        data = basket.values_list(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit',
            'recipe__amounts__amount',
        )
        return services.creating_a_shopping_list(data)
