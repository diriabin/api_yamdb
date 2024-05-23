from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from reviews.constans import (CONF_CODE_MAX_LEN, MAX_LENGTH_EMAIL,
                              MAX_LENGTH_USERNAME)
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import UsernameRegexValidator, username_is_not_me

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True
    )
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        read_only_fields = fields


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('rating',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            if Review.objects.filter(
                title=get_object_or_404(
                    Title, pk=self.context['view'].kwargs.get('title_id')),
                author=request.user
            ).exists():
                raise ValidationError('Вы не можете добавить более'
                                      'одного отзыва на произведение')
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=MAX_LENGTH_USERNAME,
        validators=(
            UsernameRegexValidator(),
            username_is_not_me
        )
    )
    confirmation_code = serializers.CharField(
        required=True,
        max_length=CONF_CODE_MAX_LEN,
    )


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=MAX_LENGTH_EMAIL)
    username = serializers.CharField(
        max_length=150,
        validators=(UsernameRegexValidator(), username_is_not_me,),
    )


class NotAdminSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=MAX_LENGTH_USERNAME,
        validators=(UsernameRegexValidator(), username_is_not_me,),
    )
    email = serializers.EmailField(
        max_length=MAX_LENGTH_EMAIL,
    )
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    bio = serializers.CharField(allow_blank=True, required=False)
    role = serializers.CharField(read_only=True)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.save()
        return instance

    class Meta(UserSerializer.Meta):
        read_only = ('role',)
