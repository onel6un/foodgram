from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Subscriptions
from rest_framework import serializers

User = get_user_model()


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    email = serializers.EmailField(required=True)

    def get_is_subscribed(self, obj):
        # Объект аутентифицированного пользователя
        user = self.context.get('request').user

        if not user.is_authenticated:
            return False

        try:
            return obj.is_subscribed
        except AttributeError:
            # Объект пользоваетля из полученного параметра
            another_user = obj

            # queryset на кого подписан аутентифицированный пользователь
            queryset_of_subscribers = Subscriptions.objects.filter(user=user)

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
