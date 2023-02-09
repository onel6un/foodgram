from rest_framework import serializers

from django.contrib.auth import get_user_model

from recipes.models import (Tags,)

User = get_user_model()


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'
