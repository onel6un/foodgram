from django.urls import path, include

from rest_framework import routers

from .views import (TagsViewSet, IngredientsViewSet, UsersViewSet,
                    RecipesViewSet, FavoriteRecipesViewSet)


APP_NAME = 'api'

router = routers.DefaultRouter()

router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('users', UsersViewSet)
router.register('recipes', RecipesViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('recipes/<int:id>/favorite/',
         (FavoriteRecipesViewSet
          .as_view({'delete': 'destroy', 'post': 'create'}))),
    path('auth/', include('djoser.urls.jwt')),
]
