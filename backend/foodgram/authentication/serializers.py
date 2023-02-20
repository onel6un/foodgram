from rest_framework import serializers

from djoser.serializers import UserCreateSerializer, UserSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    email = serializers.EmailField(required=True)

    def get_is_subscribed(self, obj):
        # Объект аутентифицированного пользователя
        user = self.context.get('request').user

        if not user.is_authenticated:
            return False
        return obj.is_subscribed

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
