from django_filters import rest_framework as filters
from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    """Кастомный фильтр для рецептов.
    Для вкладок "Избранное, "Корзина" и тегов."""
    tags = filters.MultipleChoiceFilter(field_name = 'tags__slug')
    is_favorited = filters.BooleanFilter(
        label='Favorited'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'is_favorited', 'tags')
    
    def get_is_favorited(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(favorite_recipe__user=self.request.user)
        return Recipe.objects.all()
