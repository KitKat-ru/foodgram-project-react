from django.contrib import admin

from .models import Ingredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = [
        'pk',
        'name',
        'measurement_unit',
    ]
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = [
        'pk',
        'name',
        'color',
        'slug',
    ]
    empty_value_display = '-пусто-'

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)

