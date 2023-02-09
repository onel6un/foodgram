from django.urls import path, include

from rest_framework import routers

from .views import (TagsViewSet, IngredientsViewSet)


APP_NAME = 'api'

router = routers.DefaultRouter()

router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
