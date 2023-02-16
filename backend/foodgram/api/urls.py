from django.urls import path, include

from rest_framework import routers

from .views import (TagsViewSet, IngredientsViewSet, UsersViewSet,
                    RecipesViewSet, FavoriteRecipesViewSet,
                    SubscriptionsViewSet, RecipesOnCartViewSet)


APP_NAME = 'api'

router = routers.DefaultRouter()

router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('users', UsersViewSet)
router.register('recipes', RecipesViewSet)


urlpatterns = [
    path('users/subscribe/',
         (SubscriptionsViewSet
          .as_view({'get': 'list'}))),
    path('users/<int:id>/subscribe/',
         (SubscriptionsViewSet
          .as_view({'delete': 'destroy', 'post': 'create'}))),
    path('recipes/<int:id>/favorite/',
         (FavoriteRecipesViewSet
          .as_view({'delete': 'destroy', 'post': 'create'}))),

    path('auth/', include('djoser.urls.jwt')),
    path('recipes/<int:id>/shopping_cart/',
         (RecipesOnCartViewSet
          .as_view({'delete': 'destroy', 'post': 'create'}))),
    path('recipes/download_shopping_cart/',
         (RecipesOnCartViewSet
          .as_view({'get': 'list'}))),
    path('', include(router.urls)),
]
