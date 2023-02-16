from django.urls import path

from djoser.views import UserViewSet

from .views import GetTokenView

APP_NAME = 'authentication'

urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list'})),
    path('users/<int:id>/', UserViewSet.as_view({'get': 'retrieve'})),
    path('users/register/', UserViewSet.as_view({'post': 'create'})),
    path('users/me/', UserViewSet.as_view({'get': 'me'})),
    path('users/set_password/', UserViewSet.as_view({'post': 'set_password'})),
    path('auth/token/login/', GetTokenView.as_view()),
]
