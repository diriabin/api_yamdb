from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title
from users.models import СonfirmationСode

User = get_user_model()


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(source='user.username', read_only=True)
    class Meta:
        model = СonfirmationСode
        fields = ['username', 'code']
