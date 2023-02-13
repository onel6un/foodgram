from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model

from recipes.models import (Tags, Ingredients, Recipes)
from .serializers import (TagsSerializer, IngredientsSerializer,
                          UserSerializer, RecipesSerializer,
                          RecipesSerializerForWrite)

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
