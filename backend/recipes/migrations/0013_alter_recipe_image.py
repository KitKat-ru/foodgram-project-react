# Generated by Django 3.2.14 on 2022-08-07 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_alter_recipe_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(help_text='загрузите изображение', upload_to='recipes/image/', verbose_name='фото блюда'),
        ),
    ]
