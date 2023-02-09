from rest_framework import serializers

from django.contrib.auth import get_user_model

from recipes import models

User = get_user_model()


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tags
        fields = '__All__'
