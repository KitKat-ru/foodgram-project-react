from django.core.validators import MinValueValidator
from django.db import models
from users.models import User
from ingredients.models import Ingredient, Tag


class Recipe(models.Model):
    """Модель для управления рецептами."""
    name = models.CharField(max_length=200, verbose_name='название рецепта')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='author',
        related_name='recipes',
        verbose_name='автор рецепта'
    )
    description = models.TextField(
        blank=False,
        verbose_name='описание рецепта'
    )
    image = models.ImageField(
        verbose_name='фото блюда',
        upload_to='recipes/image/',
        blank=False,
        help_text='Загрузите изображение',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient', # возможно надо будет добавить through_field = (recipe, ingredient)
        db_column='ingredient',
        verbose_name='ингредиенты для блюда'
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        db_column='tag',
        verbose_name='тег рецепта'
    )
    cooking_time = models.PositiveSmallIntegerField(
        blank=False,
        default=1,
        validators=[MinValueValidator(1), ],
        verbose_name='время приготовления блюда'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='дата публикации рецепта'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'
        ordering = ['-pub_date',]


class RecipeTag(models.Model):
    """Промежуточная таблица для связи Tag-Recipe."""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE) # релатед найм добавить
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE) # релатед найм добавить


class RecipeIngredient(models.Model):
    """Промежуточная таблица для связи Ingredient-Recipe."""
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE) # релатед найм добавить
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE) # релатед найм добавить
    amount = models.PositiveSmallIntegerField(
        blank=True,
        null=False,
        default=1,
        validators=[MinValueValidator(1), ],
        verbose_name='количество'
    )

# Выполнить pip install django-colorfield
# Добавить colorfieldвsettings.INSTALLED_APPS
# Выполнить python manage.py collectstatic
    