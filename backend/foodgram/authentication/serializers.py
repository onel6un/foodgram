from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from djoser.serializers import UserCreateSerializer, UserSerializer

from django.contrib.auth import get_user_model

from recipes.models import Subscriptions

User = get_user_model()


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    email = serializers.EmailField(required=True)

    def get_is_subscribed(self, obj):
        # Объект аутентифицированного пользователя
        auth_user = self.context.get('request').user

        # Объект пользоваетля из полученного параметра
        another_user = obj

        # queryset на кого подписан аутентифицированный пользователь
        queryset_of_subscribers = Subscriptions.objects.filter(user=auth_user)

        # Вернем True если аутентифицированный
        # пользователь подписан на переданного автора
        return queryset_of_subscribers.filter(author=another_user).exists()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')


class RegisterUserSerializer(UserCreateSerializer):
    email = serializers.EmailField(required=True)

    class Meta():
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class GetTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data.pop("refresh")
        data['auth_token'] = data.pop("access")
        return data