from django.urls import path, include

from rest_framework import routers

from .views import (TagsViewSet, IngredientsViewSet, UsersViewSet,
                    RecipesViewSet)


APP_NAME = 'api'

router = routers.DefaultRouter()

router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('users', UsersViewSet)
router.register('recipes', RecipesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.jwt'))
]
