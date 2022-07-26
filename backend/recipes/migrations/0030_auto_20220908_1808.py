# Generated by Django 3.2.14 on 2022-09-08 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0029_merge_20220905_1446'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'ordering': ['-user'], 'verbose_name': 'избранное', 'verbose_name_plural': 'объекты избранного'},
        ),
        migrations.AlterModelOptions(
            name='shoppingbasket',
            options={'ordering': ['-user'], 'verbose_name': 'корзина', 'verbose_name_plural': 'объекты списка покупок'},
        ),
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
