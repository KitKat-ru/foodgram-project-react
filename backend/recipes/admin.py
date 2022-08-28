from django.contrib import admin

from .models import Recipe, RecipeIngredient, RecipeTag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe
    list_display = [
        'pk',
        'name',
        'author',
        'pub_date',
        'counts_favorite',
        'counts_shopping_basket',
    ]
    inlines = [RecipeIngredientInline, RecipeTagInline]
    search_fields = ('author', 'name')
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ['counts_favorite', 'counts_shopping_basket']
    empty_value_display = '-пусто-'

    def counts_favorite(self, obj):
        return obj.selected.count()

    def counts_shopping_basket(self, obj):
        return obj.shopping_basket.count()


admin.site.register(Recipe, RecipeAdmin)
