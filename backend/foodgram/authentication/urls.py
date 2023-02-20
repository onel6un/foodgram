from django.urls import path, include

from djoser.views import UserViewSet

from .views import CustomUserViewSet

APP_NAME = 'authentication'

urlpatterns = [
    path('users/', CustomUserViewSet.as_view({'get': 'list'})),
    path('users/<int:id>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('users/register/', UserViewSet.as_view({'post': 'create'})),
    path('users/me/', UserViewSet.as_view({'get': 'me'})),
    path('users/set_password/', UserViewSet.as_view({'post': 'set_password'})),
    path('auth/', include('djoser.urls.authtoken')),
]
