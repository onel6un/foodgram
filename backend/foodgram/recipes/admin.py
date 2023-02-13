from django.contrib import admin

from .models import (TagsForRecipe, Recipes, HelpIngredients, Tags,
                     Ingredients, Subscriptions, IngredientAmount,
                     FavoritRecipes)


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
    list_display = ('name', 'author')
    list_filter = ('name', 'tags', 'author')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email',
                    'first name', 'last name',)
    list_filter = ('username', 'email')


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount')


class FavoritRecipesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipes')


admin.site.register(Tags, TagsAdmin)
admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(Recipes, RecipesAdmin)
admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(FavoritRecipes, FavoritRecipesAdmin)
