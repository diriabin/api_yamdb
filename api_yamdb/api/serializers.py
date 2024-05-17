import re

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title

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
