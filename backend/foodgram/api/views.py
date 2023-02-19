from django.http import HttpResponse
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions

from .permissions import AuthorOrReadOnly, ReadOnly
from recipes.models import (Tags, Ingredients, Recipes, FavoritRecipes,
                            Subscriptions, RecipesOnCart)
from .serializers import (TagsSerializer, IngredientsSerializer,
                          UserSerializer, RecipesSerializer,
                          RecipesSerializerForWrite, FavoritRecipesSerializers,
                          SubscriptionsSerializer, RecipesOnCartSerializer)

User = get_user_model()


class UsersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (ReadOnly,)


class IngredientsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                         mixins.RetrieveModelMixin):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (ReadOnly,)


class RecipesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Recipes.objects.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        return (AuthorOrReadOnly(),)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipesSerializer
        return RecipesSerializerForWrite

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )


class FavoriteRecipesViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                             mixins.DestroyModelMixin):
    serializer_class = FavoritRecipesSerializers
    lookup_field = 'recipe'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        recipe_id = self.kwargs.get('id')
        user_obj = self.request.user
        queryset = (FavoritRecipes.objects
                    .filter(user=user_obj)
                    .filter(recipe=recipe_id))
        return queryset

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('id')
        serializer.save(
            user=self.request.user,
            recipe=Recipes.objects.get(pk=recipe_id)
        )


class SubscriptionsViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                           mixins.DestroyModelMixin, mixins.ListModelMixin):
    serializer_class = SubscriptionsSerializer
    lookup_field = 'author'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        user = self.request.user
        queryset = Subscriptions.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        author_id = self.kwargs.get('id')
        author_obj = User.objects.get(pk=author_id)
        serializer.save(
            user=self.request.user,
            author=author_obj
        )


class RecipesOnCartViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                           mixins.DestroyModelMixin, mixins.ListModelMixin):
    serializer_class = RecipesOnCartSerializer
    lookup_field = 'recipe'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        user = self.request.user
        queryset = RecipesOnCart.objects.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('id')
        recipe_obj = Recipes.objects.get(pk=recipe_id)
        serializer.save(
            user=self.request.user,
            recipe=recipe_obj
        )

    def list(self, request, *args, **kwargs):
        '''Отправим в ответе файл со списком игредиентов'''
        queryset = self.get_queryset()

        dict_of_ingred = {}

        # Переберем в цикле queryset ингредиентов в корзине пользователя
        for recipe_on_cart in queryset:
            # Переберем в цикле игредиенты из рецепта
            for ingredient_obj in recipe_on_cart.recipe.ingredients.all():
                name = ingredient_obj.ingredient.name
                measurement_unit = ingredient_obj.ingredient.measurement_unit
                amount = ingredient_obj.amount

                # Создадим ключ для словаря игредиентов
                key = f'{name}({measurement_unit})'

                # Если данный игредиент есть в словаре по ключу,
                # добавим количество ингрединта в этот ключ
                if key in dict_of_ingred.keys():
                    dict_of_ingred[key] = dict_of_ingred[key] + amount
                else:
                    dict_of_ingred[key] = amount

        '''cat_book = open('cat_book.txt', 'w+')
        try:
            for ingredient_name, amount in dict_of_ingred.items():
                cat_book.write(f'{ingredient_name} — {amount} \n')

            #file_data = cat_book.read()
            print(cat_book)
            file_data = '111'
            response = HttpResponse(file_data, content_type='text/plain')
            response['Content-Disposition'] = (
                'attachment; filename="список_ингредиентов.txt"'
            )
        finally:
            cat_book.close()'''

        # Составим строковый список ингрединтов
        text = ''
        for ingredient_name, amount in dict_of_ingred.items():
            text += f'{ingredient_name} — {amount} \n'

        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = (
                'attachment; filename="список_ингредиентов.txt"'
            )
        return response
