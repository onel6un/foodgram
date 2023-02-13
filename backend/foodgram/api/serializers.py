from rest_framework import serializers

from django.contrib.auth import get_user_model

from recipes.models import (Tags, Ingredients, Recipes, Subscriptions,
                            IngredientAmount, FavoritRecipes, RecipesOnCart,
                            TagsForRecipe, HelpIngredients)


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


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
        source='ingredient'
    )
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True)
    ingredients = IngredientAmountSerializer(many=True)
    is_favorited = serializers.ReadOnlyField()
    is_in_shopping_cart = serializers.ReadOnlyField()
    author = UserSerializer()

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def to_representation(self, instance):
        """Принимает экземпляр объекта, который требует сериализации,
        и должен вернуть примитивное представление. Добавим в словарь
        данные о наличии рецепта в избранном и корзине"""
        ret = super().to_representation(instance)

        # Объект аутентифицированного пользователя
        auth_user = self.context.get('request').user

        # Id Рецепта из полученного параметра
        recipe_current_id = ret.get('id')

        # queryset рецептов в избранном у аутентифицированного пользователя
        queryset_of_favorite = FavoritRecipes.objects.filter(user=auth_user)

        # queryset рецептов в корзине у аутентифицированного пользователя
        queryset_on_cart = RecipesOnCart.objects.filter(user=auth_user)

        # вернем и добавим в словарь True если аутентифицированный
        # пользователь подписан на переданного автора
        ret['is_favorited'] = (
            queryset_of_favorite
            .filter(recipes=recipe_current_id)
            .exists()
        )

        ret['is_in_shopping_cart'] = (
            queryset_on_cart
            .filter(recipes=recipe_current_id)
            .exists()
        )
        return ret


class RecipesSerializerForWrite(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tags.objects.all(),
        required=True
    )
    ingredients = IngredientAmountSerializer(many=True, required=True)
    author = UserSerializer(read_only=True)

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                'Укажите теги'
            )
        return value

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                'В рецепте не могут отсутствовать ингредиенты'
            )
        return value

    class Meta:
        model = Recipes
        fields = ('tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time')

    def create(self, validated_data):
        ingredients_value = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        recipe = Recipes.objects.create(**validated_data)

        for tag in tags:
            # создадим запись в вспомогательную таблицу тегов
            TagsForRecipe.objects.create(recipe=recipe, tag=tag)

        # Переберем в цикле ингредиенты и их количество
        for ingredient_value in ingredients_value:
            ingredient = ingredient_value.get('ingredient')
            amount = ingredient_value.get('amount')

            # Получим queryset из таблицы с количеством ингредиента
            current_ingredient_value = (IngredientAmount.objects
                                        .filter(ingredient=ingredient)
                                        .filter(amount=amount))

            # Выполним проверку на наличее записи ингредиента с таким кол-вом,
            # если такой записи нет, создадим.
            if not current_ingredient_value.exists():
                # такой записи нет:
                amount_ingredient = IngredientAmount.objects.create(
                    ingredient=ingredient,
                    amount=amount
                )

                HelpIngredients.objects.create(
                    recipe=recipe,
                    ingredient=amount_ingredient
                )
            else:
                # такая запись есть, добавим в вспомгательную таблицу:
                HelpIngredients.objects.create(
                    recipe=recipe,
                    ingredient=current_ingredient_value.first()
                )

        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')

        ingredients_data = validated_data.pop('ingredients')

        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        instance.imahe = validated_data.get('image', instance.image)
        instance.save()

        for tag in TagsForRecipe.objects.filter(recipe=instance):
            tag.delete()

        for tag in tags_data:
            TagsForRecipe.objects.create(recipe=instance, tag=tag)

        for ing_value in HelpIngredients.objects.filter(recipe=instance):
            ing_value.delete()
        
        for ingredient_value in ingredients_data:
            ingredient = ingredient_value.get('ingredient')
            amount = ingredient_value.get('amount')

            # Получим queryset из таблицы с количеством ингредиента
            current_ingredient_value = (IngredientAmount.objects
                                        .filter(ingredient=ingredient)
                                        .filter(amount=amount))

            # Выполним проверку на наличее записи ингредиента с таким кол-вом,
            # если такой записи нет, создадим.
            if not current_ingredient_value.exists():
                # такой записи нет:
                amount_ingredient = IngredientAmount.objects.create(
                    ingredient=ingredient,
                    amount=amount
                )

                HelpIngredients.objects.create(
                    recipe=instance,
                    ingredient=amount_ingredient
                )
            else:
                # такая запись есть, добавим в вспомгательную таблицу:
                HelpIngredients.objects.create(
                    recipe=instance,
                    ingredient=current_ingredient_value.first()
                )

        return instance

    def to_representation(self, instance):
        """Принимает экземпляр объекта, который требует сериализации,
        и должен вернуть примитивное представление."""
        tags = instance.tags.all()
        ret = super().to_representation(instance)
        serializer = TagsSerializer(tags, many=True)
        ret['tags'] = serializer.data
        return ret
