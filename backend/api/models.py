from django.db import models
from recipes.models import Recipe
from users.models import User


class Favorite(models.Model):
    """Модель для реализации добавления рецептов в "Избранное"."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='selecting'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='selected'
    )

    class Meta:
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
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shopping_basket'
            ),
        ]


class Subscription(models.Model):
    """Модель для реализации подписки на авторов рецептов."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following',
        verbose_name='автор рецепта',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follower'
            ),
        ]