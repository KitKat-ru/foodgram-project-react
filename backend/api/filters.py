from django_filters import rest_framework as filters
from ingredients.models import Ingredient
from recipes.models import Recipe
from django_filters.rest_framework import FilterSet, filters

class RecipeFilter(FilterSet):
    """Кастомный фильтр для рецептов.
    Для вкладок "Избранное, "Корзина" и тегов."""
    tags = filters.MultipleChoiceFilter(field_name='tags__slug', )
    is_favorited = filters.BooleanFilter(
        label='Favorited',
        method='get_is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        label='ShoppingCart',
        method='get_is_in_shopping_cart',
    )

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'tags', 'is_in_shopping_cart', )
    
    def get_is_favorited(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(selected__user=self.request.user)
        return Recipe.objects.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(shopping_basket__user=self.request.user)
        return Recipe.objects.all()


class SearchIngredientFilter(FilterSet):
    """Кастомный фильтр для ингридиентов."""
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name', )