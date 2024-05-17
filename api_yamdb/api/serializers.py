import re

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title
from users.models import СonfirmationСode

User = get_user_model()

SLUG_PATTERN = r'^[-a-zA-Z0-9_]+$'


class TitleSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')

    def validate_slug(self, value):
        if re.fullmatch(SLUG_PATTERN, value):
            return value
        raise serializers.ValidationError(
            'Для слага можно использовать только: A-Z, a-z, 0-9, _'
        )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate_slug(self, value):
        if re.fullmatch(SLUG_PATTERN, value):
            return value
        raise serializers.ValidationError(
            'Для слага можно использовать только: A-Z, a-z, 0-9, _'
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(source='user.username', read_only=True)

    class Meta:
        model = СonfirmationСode
        fields = ['username', 'confirmation_code']
