from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Tag(models.Model):
    """Модель для тегов."""
    name = models.CharField(
        max_length=128,
        unique=True,
    )
    slug = models.SlugField(
        max_length=128,
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Tag color',
        unique=True,
    )

    class Meta:
        ordering = ('slug',)
        constraints = [
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_slug',
            )
        ]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель для ингридиентов."""
    name = models.CharField(
        max_length=128,
        unique=True,
    )
    measurement = models.CharField(
        max_length=16,
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель для рецептов."""
    name = models.CharField(
        max_length=200,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    tag = models.ManyToManyField(
        Tag,
        through='TagsRecipe',
        related_name='recipes',
    )
    ingridients = models.ManyToManyField(
        Ingredient,
        through='IngredientsRecipe',
        related_name='recipes',
    )
    text = models.TextField(
        max_length=1024,
        null=False,
    )
    cooking_time = models.DecimalField(
        max_digits=5,
        decimal_places=1,
    )
    image = models.ImageField(
        upload_to='recipes/',
        null=True,
        blank=True,
    )


class TagsRecipe(models.Model):
    """Модель для тегов рецептов."""
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


class IngredientsRecipe(models.Model):
    """Модель для ингридиентов рецептов."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe'
            )
        ]


class Subscribe(models.Model):
    """Модель для подписок."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['author', 'user'],
            name='unique_object',
        )]


class FavoriteRecipe(models.Model):
    """Модель для избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=False, null=False,
        related_name='favorite_recipes',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite',
            )
        ]


class ShoppingCart(models.Model):
    """Модель для корзины покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_cart',
            )
        ]
