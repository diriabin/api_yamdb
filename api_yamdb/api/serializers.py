from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from .mixins import UsernameMixin
from reviews.constans import MAX_LENGTH_EMAIL, MAX_LENGTH_USERNAME
from reviews.models import Category, Genre, Title, Review, Comment
from reviews.validators import validate_confirmation_code

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
    rating = serializers.IntegerField(read_only=True)
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


class ReviewSerializer(serializers.ModelSerializer, UsernameMixin):
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        if Review.objects.filter(
                title=get_object_or_404(
                    Title, pk=self.context['view'].kwargs.get('title_id')
                ), author=request.user
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


class GetTokenSerializer(serializers.Serializer, UsernameMixin):
    username = serializers.CharField(required=True,
                                     max_length=MAX_LENGTH_USERNAME)
    confirmation_code = serializers.CharField(
        required=True,
        max_length=settings.CONF_CODE_MAX_LEN,
        validators=(validate_confirmation_code,)
    )

    def validate_confirmation_code(self, pin_code):
        if pin_code == settings.DEFAULT_CONF_CODE:
            raise ValidationError(
                'Ошибка. Сначала получите код подтверждения.'
            )
        invalid_chars = re.findall(
            fr"'{re.escape(settings.DIGS)}\s'", pin_code
        )
        if invalid_chars:
            raise ValidationError(
                f'Код не должен содержать символы {invalid_chars}'
            )
        return pin_code

class SignUpSerializer(serializers.Serializer, UsernameMixin):
    username = serializers.CharField(required=True,
                                     max_length=MAX_LENGTH_USERNAME)
    email = serializers.EmailField(required=True,
                                   max_length=MAX_LENGTH_EMAIL)


class NotAdminSerializer(serializers.ModelSerializer, UsernameMixin):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)
