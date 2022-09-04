from django import forms
from django.contrib import admin

from .models import (Favorite, Recipe, RecipeIngredient, RecipeTag,
                     ShoppingBasket)


class IngredientsInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                pass
        if count < 1:
            raise forms.ValidationError('Добавьте ингредиенты')


class TagsInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                pass
        if count < 1:
            raise forms.ValidationError('Добавьте теги')


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    formset = IngredientsInlineFormset
    extra = 2


class RecipeTagInline(admin.TabularInline):
    model = RecipeTag
    formset = TagsInlineFormset
    extra = 3


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
    search_fields = ('name', 'author__username', 'tags__name', )
    list_filter = ('author', 'name', 'tags')
    readonly_fields = ['counts_favorite', 'counts_shopping_basket']
    empty_value_display = '-пусто-'

    def counts_favorite(self, obj):
        return obj.selected.count()

    def counts_shopping_basket(self, obj):
        return obj.shopping_basket.count()


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = [
        'pk',
        'user',
        'recipe',
    ]


class ShoppingBasketAdmin(admin.ModelAdmin):
    model = ShoppingBasket
    list_display = [
        'pk',
        'user',
        'recipe',
    ]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingBasket, ShoppingBasketAdmin)
