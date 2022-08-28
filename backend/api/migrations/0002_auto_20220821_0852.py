# Generated by Django 3.2.14 on 2022-08-21 08:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0015_rename_description_recipe_text'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingbasket',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_basket', to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='shoppingbasket',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_basket', to=settings.AUTH_USER_MODEL),
        ),
    ]
