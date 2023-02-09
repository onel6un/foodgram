from django.urls import path, include

from rest_framework import routers

from .views import TagsViewSet


APP_NAME = 'api'

router = routers.DefaultRouter()

router.register('tags', TagsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
