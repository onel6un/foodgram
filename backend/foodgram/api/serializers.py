from rest_framework import serializers

from django.contrib.auth import get_user_model

from recipes.models import (Tags, Ingredients, Recipes, Subscriptions)


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'password')

    def to_representation(self, instance):
        """Принимает экземпляр объекта, который требует сериализации,
        и должен вернуть примитивное представление. Добавим в словарь
        данные о наличии подписки на автора рецептов"""
        ret = super().to_representation(instance)

        # Объект аутентифицированного пользователя
        auth_user = self.context.get('request').user

        # Объект пользоваетля из полученного параметра
        another_user = User.objects.get(pk=ret.get('id'))

        # queryset на кого подписан аутентифицированный пользователь
        queryset_of_subscribers = Subscriptions.objects.filter(user=auth_user)

        # вернем и добавим в словарь True если аутентифицированный
        # пользователь подписан на переданного автора
        ret['is_subscribed'] = (
            queryset_of_subscribers
            .filter(author=another_user)
            .exists()
        )

        return ret

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'


"""class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer()

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')"""
