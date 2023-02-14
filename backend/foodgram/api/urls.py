from django.urls import path, include

from rest_framework import routers

from .views import (TagsViewSet, IngredientsViewSet, UsersViewSet,
                    RecipesViewSet, FavoriteRecipesViewSet,
                    SubscriptionsViewSet)


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
    path('', include(router.urls)),
    path('recipes/<int:id>/favorite/',
         (FavoriteRecipesViewSet
          .as_view({'delete': 'destroy', 'post': 'create'}))),

    path('auth/', include('djoser.urls.jwt')),
]
