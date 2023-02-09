from django.contrib import admin

from . import models


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class TagsInLine(admin.TabularInline):
    model = models.TagsForRecipe
    extra = 1


class IngredientsInLine(admin.TabularInline):
    model = models.AmountIngredients
    extra = 1
    raw_id_fields = ('ingredient',)


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


admin.site.register(models.Tags, TagsAdmin)
admin.site.register(models.Ingredients, IngredientsAdmin)
admin.site.register(models.Recipes, RecipesAdmin)