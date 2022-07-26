from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        blank=False, null=False,
        unique=True, max_length=254,
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=False,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=False,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_login_fields',

            ),
        ]

    def __str__(self):
        return self.username


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

    def __str__(self):
        return f'Связь {self.user} - {self.following}'
