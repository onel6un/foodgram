import django_filters
from django_filters import rest_framework

from recipes.models import Recipes


class RecipesFilterSet(rest_framework.FilterSet):
    """Зададим фильтрсет для вьюсета RecipesViewSet"""
    tags = django_filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='contains'
    )

    class Meta:
        model = Recipes
        fields = ('tags', 'author')
