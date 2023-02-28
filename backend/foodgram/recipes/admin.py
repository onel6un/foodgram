from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import (FavoritRecipes, HelpIngredients, IngredientAmount,
                     Ingredients, Recipes, RecipesOnCart, Subscriptions, Tags,
                     TagsForRecipe)

User = get_user_model()


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


class TagsInLine(admin.TabularInline):
    model = TagsForRecipe
    extra = 1


class IngredientsInLine(admin.TabularInline):
    model = HelpIngredients
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    inlines = (
        IngredientsInLine,
        TagsInLine
    )
    list_display = ('name', 'author', 'in_favorited')
    list_filter = ('name', 'tags', 'author')
    readonly_fields = ('in_favorited',)

    def in_favorited(self, obj):
        return obj.favorits.all().count()


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email',
                    'first_name', 'last_name', 'date_joined')
    list_filter = ('username', 'email')


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount')


class FavoritRecipesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class RecipesOnCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


admin.site.register(Tags, TagsAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(FavoritRecipes, FavoritRecipesAdmin)
admin.site.register(RecipesOnCart, RecipesOnCartAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
