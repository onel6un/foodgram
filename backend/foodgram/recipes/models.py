from django.contrib.auth import get_user_model
from django.db import models

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
    name = models.CharField(max_length=200, db_index=True)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.ingredient} - {self.amount}'


class Recipes(models.Model):
    """Модель рецептов"""
    name = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    text = models.TextField()
    cooking_time = models.IntegerField()
    ingredients = models.ManyToManyField(
        IngredientAmount,
        through='HelpIngredients'
    )
    tags = models.ManyToManyField(
        Tags,
        through='TagsForRecipe'
    )
    image = models.ImageField(
        upload_to='recipes/image/',
        blank=True
    )
    pub_date = models.DateField(auto_now_add=True, db_index=True)

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


class HelpIngredients(models.Model):
    """Модель отношения ингредиента и рецепта (вспомогательная модель)"""
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        IngredientAmount,
        on_delete=models.CASCADE
    )


class FavoritRecipes(models.Model):
    """Модель избранных рецептов"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorits'
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorits'
    )

    def __str__(self) -> str:
        return f'В избранном у {self.user.username} {self.recipe.name}'


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

    def __str__(self) -> str:
        return f'{self.user} to {self.author}'


class RecipesOnCart(models.Model):
    """Рецепты в корзине пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f'{self.user} to {self.recipe}'
