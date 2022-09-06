# Generated by Django 3.2.14 on 2022-09-03 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0024_alter_recipe_cooking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.SmallIntegerField(default=1, verbose_name='время приготовления блюда'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.SmallIntegerField(blank=True, default=1, verbose_name='количество'),
        ),
    ]