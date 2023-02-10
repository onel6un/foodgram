from rest_framework import viewsets
from rest_framework import mixins

from django.contrib.auth import get_user_model

from recipes.models import (Tags, Ingredients)
from .serializers import (TagsSerializer, IngredientsSerializer,
                          UserSerializer)

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
