from rest_framework import viewsets
from rest_framework import mixins

from recipes.models import Tags
from .serializers import TagsSerializer


class TagsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
