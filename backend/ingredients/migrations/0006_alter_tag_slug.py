# Generated by Django 3.2.14 on 2022-08-21 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0005_remove_ingredient_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='слаг тега'),
        ),
    ]
