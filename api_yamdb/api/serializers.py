from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title


class TitleSerializer(serializers.Serializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class GenreSerializer(serializers.Serializer):

    class Meta:
        model = Genre
        fields = '__all__'


class CategorySerializer(serializers.Serializer):

    class Meta:
        model = Category
        fields = '__all__'
