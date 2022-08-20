from colorfield.fields import ColorField
from django.db import models


class Ingredient(models.Model):
    """Модель описывающая продукт."""
    name = models.CharField(max_length=128, verbose_name='наименование ингредиента')
    measurement_unit = models.CharField(max_length=128, verbose_name='единица измерения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        ordering = ['-name',]


class Tag(models.Model):
    """Модель описывающая тег."""
    COLOR_PALETTE = [
        ("#49b64e", "green", ), 
        ("#e26c2d", "orange", ),
        ("#8775d2", "purple", ),
    ]
    name = models.CharField(max_length=128, verbose_name='наименование тега')
    color = ColorField(samples=COLOR_PALETTE, verbose_name='цвет тега')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг тега'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'
        ordering = ['-name',]

