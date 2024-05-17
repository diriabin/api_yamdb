from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from reviews.models import Category, Genre, Title, Review, Comment
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
        exclude = ('id',)
        lookup_field = 'slug'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    username = serializers.SlugField(source='user.username', read_only=True)
    class Meta:
        model = СonfirmationСode
        fields = ['username', 'confirmation_code']


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'


# class CategorySerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Category
#         exclude = ('id',)
#         lookup_field = 'slug'
#         extra_kwargs = {
#             'url': {'lookup_field': 'slug'}
#         }
