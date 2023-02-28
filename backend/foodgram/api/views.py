from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef
from django.db.models.query import Prefetch
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (FavoritRecipes, Ingredients, Recipes,
                            RecipesOnCart, Subscriptions, Tags)
from rest_framework import filters, mixins, permissions, viewsets

from . import filter_sets
from .pagination import CustomPagination
from .permissions import AuthorOrReadOnly, ReadOnly
from .serializers import (FavoritRecipesSerializers, IngredientsSerializer,
                          RecipesOnCartSerializer, RecipesSerializer,
                          RecipesSerializerForWrite, SubscriptionsSerializer,
                          TagsSerializer)

User = get_user_model()


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
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class RecipesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Recipes.objects.all()
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filter_sets.RecipesFilterSet

    def get_queryset(self):
        '''Явно определим бекенд фильтрации, по параметрам
        is_favorited, is_in_shopping_cart'''
        # Получим объект пользователя из запроса
        user = self.request.user
        if self.request.user.is_authenticated:
            # Subquery: пользователь - автор в подписках
            subquery_subscr = Subscriptions.objects.filter(
                user=user,
                author=OuterRef('pk')
            )
            # Subquery: пользоаватель - рецепт в избранном
            subquery_favorite = FavoritRecipes.objects.filter(
                user=user,
                recipe=OuterRef('pk')
            )
            # Subquery: пользоаватель - рецепт в корзине
            subquery_cart = RecipesOnCart.objects.filter(
                user=user,
                recipe=OuterRef('pk')
            )
            # Добавим в аннотации два парметра о нахождении данного рецепта
            # в избранном и корзине
            queryset = (Recipes.objects
                        .prefetch_related('tags')
                        .prefetch_related('ingredients')
                        .prefetch_related('ingredients__ingredient')
                        .prefetch_related(
                            Prefetch(
                                'author',
                                User.objects.annotate(
                                    is_subscribed=Exists(subquery_subscr)
                                )
                            )
                        )
                        .annotate(
                            in_favorite=Exists(subquery_favorite),
                            is_in_shopping_cart=Exists(subquery_cart)
                        )
                        .order_by('pub_date')
                        )
        else:
            queryset = (Recipes.objects
                        .prefetch_related('tags')
                        .prefetch_related('ingredients')
                        .prefetch_related('ingredients__ingredient')
                        )

        # Получим query params из запроса
        is_favorited_query = self.request.query_params.get('is_favorited')
        is_in_shopping_cart_query = self.request.query_params.get(
            'is_in_shopping_cart'
        )

        # Создадим два пустых QS
        filter_favorite_queryset = Recipes.objects.none()
        filter_cart_queryset = Recipes.objects.none()

        # Если параметр фильтрации не None и равен '0' или '1'
        if is_favorited_query is not None and is_favorited_query in ('0', '1'):
            # Получим QS объектов: текущий пользователь - рецепт в избранном
            favorit_recipes = (FavoritRecipes.objects.filter(user=user)
                               .values_list('recipe'))

            if is_favorited_query == '1':
                # Отфильтруем из начального QS обекты которые есть в корзине
                favorite_qrst = queryset.filter(id__in=favorit_recipes)
            else:
                # Исключим из начального QS обекты которые есть в корзине
                favorite_qrst = queryset.exclude(id__in=favorit_recipes)
            # Объединим пустое множество с полученным
            filter_favorite_queryset = (filter_favorite_queryset
                                        .union(favorite_qrst))

        # Если параметр фильтрации не None и равен '0' или '1'
        if (is_in_shopping_cart_query is not None
                and is_in_shopping_cart_query in ('0', '1')):
            # Получим QS объектов: текущий пользователь - рецепт в корзине
            recipes_on_cart = (RecipesOnCart.objects.filter(user=user)
                               .values_list('recipe'))

            if is_in_shopping_cart_query == '1':
                # Отфильтруем из начального QS обекты которые есть в корзине
                on_cart_qrst = queryset.filter(id__in=recipes_on_cart)
            else:
                # Исключим из начального QS обекты которые есть в корзине
                on_cart_qrst = queryset.exclude(id__in=recipes_on_cart)
            # Объединим пустое множество с полученным
            filter_cart_queryset = filter_cart_queryset.union(on_cart_qrst)

        # Если переданны оба параметра, венем пересечение множеств
        if (is_in_shopping_cart_query is not None
                and is_favorited_query is not None):
            return filter_favorite_queryset.intersection(filter_cart_queryset)

        # Если переданны один параметр, венем объединение множеств
        if (is_in_shopping_cart_query is not None
                or is_favorited_query is not None):
            return filter_favorite_queryset.union(filter_cart_queryset)

        return queryset

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
        return (FavoritRecipes.objects
                .filter(user=user_obj)
                .filter(recipe=recipe_id))

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
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        subquery_subscr = Subscriptions.objects.filter(
            user=user,
            author=OuterRef('pk')
        )
        return (Subscriptions.objects
                .prefetch_related(
                    Prefetch(
                        'author',
                        User.objects.annotate(
                            is_subscribed=Exists(subquery_subscr)
                        )
                    )
                )
                .prefetch_related(
                    Prefetch(
                        'author__recipes',
                        Recipes.objects.order_by('-pub_date')
                    )
                )
                .annotate(count_rec=Count('author__recipes'))
                .filter(user=user))

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
        return RecipesOnCart.objects.filter(user=user)

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

        # Составим строковый список ингрединтов
        text = ''
        for ingredient_name, amount in dict_of_ingred.items():
            text += f'{ingredient_name} — {amount} \n'

        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="список_ингредиентов.txt"'
        )
        return response
