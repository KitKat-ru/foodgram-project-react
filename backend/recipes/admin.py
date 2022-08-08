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
        'description',
        'image',
        'cooking_time',
        'pub_date',
    ]
    inlines = (RecipeIngredientInline, RecipeTagInline, )
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
