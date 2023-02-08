from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Tags(models.Model):
    """Теги для присвоения рецептам"""
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, blank=True, null=True)
    slug = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name


class Ingredients(models.Model):
    """Модель ингридиентов"""
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Recipes(models.Model):
    """Модель рецептов"""
    name = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(
        Ingredients,
        through='AmountIngredients'
    )
    tags = models.ManyToManyField(
        Tags,
        through='TagsForRecipe'
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True
    )
    is_favorited = models.BooleanField(
        default=False,
        verbose_name='Нахождение в избранном'
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name='Нахождение в корзине'
    )

    def __str__(self) -> str:
        return self.name


class TagsForRecipe(models.Model):
    """Модель тегов для рецепта (вспомогательная модель)"""
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE
    )


class AmountIngredients(models.Model):
    """Модель количества ингредиента (вспомогательная модель)"""
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()


class FavoritRecipes(models.Model):
    """Модель избранных рецептов"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipes = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )


class Subscriptions(models.Model):
    """модель подписки на авторов"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )
