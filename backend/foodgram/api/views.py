from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status

from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from recipes.models import (Tags, Ingredients, Recipes, FavoritRecipes,
                            Subscriptions)
from .serializers import (TagsSerializer, IngredientsSerializer,
                          UserSerializer, RecipesSerializer,
                          RecipesSerializerForWrite, FavoritRecipesSerializers,
                          SubscriptionsSerializer)

User = get_user_model()


class UsersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer


class IngredientsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                         mixins.RetrieveModelMixin):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer


class RecipesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Recipes.objects.all()
    permission_classes = (AllowAny,)

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

    def get_queryset(self):
        recipe_id = self.kwargs.get('id')
        queryset = FavoritRecipes.objects.filter(recipes=recipe_id)
        return queryset

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('id')
        serializer.save(
            user=self.request.user,
            recipes=Recipes.objects.get(pk=recipe_id)
        )

    def destroy(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('id')
        FavoritRecipes.objects.get(recipes=recipe_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionsViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin,
                           mixins.DestroyModelMixin, mixins.ListModelMixin):
    serializer_class = SubscriptionsSerializer

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

    def destroy(self, request, *args, **kwargs):
        author_id = self.kwargs.get('id')
        user_obj = self.request.user
        (Subscriptions.objects
            .filter(user=user_obj)
            .filter(author=author_id)
            .delete())

        return Response(status=status.HTTP_204_NO_CONTENT)
