# Generated by Django 3.2.14 on 2022-09-03 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0022_alter_recipeingredient_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.SmallIntegerField(blank=True, verbose_name='количество'),
        ),
    ]
