from django.urls import include, path
from rest_framework import routers

from .views import (FavoriteRecipesViewSet, IngredientsViewSet,
                    RecipesOnCartViewSet, RecipesViewSet, SubscriptionsViewSet,
                    TagsViewSet)

APP_NAME = 'api'

router = routers.DefaultRouter()

router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipesViewSet)


urlpatterns = [
    path('', include('authentication.urls')),
    path('users/subscriptions/',
         (SubscriptionsViewSet
          .as_view({'get': 'list'}))),
    path('users/<int:id>/subscribe/',
         (SubscriptionsViewSet
          .as_view({'delete': 'destroy', 'post': 'create'}))),
    path('recipes/<int:id>/favorite/',
         (FavoriteRecipesViewSet
          .as_view({'delete': 'destroy', 'post': 'create'}))),
    path('recipes/<int:id>/shopping_cart/',
         (RecipesOnCartViewSet
          .as_view({'delete': 'destroy', 'post': 'create'}))),
    path('recipes/download_shopping_cart/',
         (RecipesOnCartViewSet
          .as_view({'get': 'list'}))),
    path('', include(router.urls)),
]
