# Generated by Django 3.2.14 on 2022-08-07 12:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        ('ingredients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(db_column='author', on_delete=django.db.models.deletion.CASCADE, related_name='recipes_recipe', to=settings.AUTH_USER_MODEL, verbose_name='автор рецепта'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(db_column='ingredient', through='recipes.RecipeIngredient', to='ingredients.Ingredient', verbose_name='ингредиенты для блюда'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(db_column='tag', through='recipes.RecipeTag', to='ingredients.Tag', verbose_name='тег рецепта'),
        ),
    ]
