from django.db import models

from ingredients.models import Ingredient, Tag
from users.models import User


class Recipe(models.Model):
    """Модель для управления рецептами."""
    name = models.CharField(max_length=200, verbose_name='название рецепта')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='author',
        related_name='recipes',
        verbose_name='автор рецепта',
    )
    text = models.TextField(
        blank=False,
        verbose_name='описание рецепта',
    )
    image = models.ImageField(
        verbose_name='фото блюда',
        upload_to='recipes/image/',
        blank=False,
        help_text='загрузите изображение',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        db_column='ingredient',
        verbose_name='ингредиенты для блюда',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        db_column='tag',
        verbose_name='тег рецепта',
    )
    cooking_time = models.SmallIntegerField(
        blank=False,
        default=0,
        verbose_name='время приготовления блюда',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='дата публикации рецепта',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['-pub_date']


class RecipeTag(models.Model):
    """Промежуточная модель для связи Tag-Recipe."""
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='recipe_tags',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_tags',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'recipe'], name='unique_tags'
            ),
        ]


class RecipeIngredient(models.Model):
    """Промежуточная модель для связи Ingredient-Recipe."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amounts',
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amounts',
    )
    amount = models.SmallIntegerField(
        blank=True,
        default=0,
        null=False,
        verbose_name='количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'], name='unique_ingredients'
            ),
        ]

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} - {self.amount}'


class Favorite(models.Model):
    """Модель для реализации добавления рецептов в "Избранное"."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='selecting'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='selected'
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'объекты избранного'
        ordering = ['-user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorites'
            ),
        ]


class ShoppingBasket(models.Model):
    """Модель для реализации добавления рецептов в "Корзину"."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_basket'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_basket'
    )

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'объекты списка покупок'
        ordering = ['-user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shopping_basket'
            ),
        ]
