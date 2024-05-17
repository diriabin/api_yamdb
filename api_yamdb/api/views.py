import random

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view
from rest_framework import mixins, viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdminOrReadOnly, IsAdminModeratorOwnerOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          UserSerializer, ConfirmationCodeSerializer,
                          CommentSerializer, ReviewSerializer)
from reviews.models import Category, Genre, Title, Review
from users.models import СonfirmationСode

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


@api_view(['PATCH', 'DELETE'])
def genre_delete(request, genre_slug):
    user = request.user

    if not user.is_authenticated:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif request.method == 'DELETE' and user.role == 'admin':
        get_object_or_404(Genre, slug=genre_slug).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method in ('PATCH', 'DELETE') and user.role != 'admin':
        return Response(status=status.HTTP_403_FORBIDDEN)

    return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['PATCH', 'DELETE'])
def category_delete(request, category_slug):
    user = request.user

    if not user.is_authenticated:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    elif request.method == 'DELETE' and user.role == 'admin':
        get_object_or_404(Category, slug=category_slug).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method in ('PATCH', 'DELETE') and user.role != 'admin':
        return Response(status=status.HTTP_403_FORBIDDEN)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CreateUserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        username = request.data.get('username')

        if not User.objects.filter(username=username).exists():
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

        user = get_object_or_404(User, username=username)
        code = random.randint(100, 999)
        if СonfirmationСode.objects.filter(user=user).exists():
            СonfirmationСode.objects.filter(user=user).delete()
        СonfirmationСode.objects.create(user=user, code=code)

        send_mail(
            subject='Код для регистрации',
            message=f'confirmation_code: {code}, username: {username}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.data.get('email')],
            fail_silently=False,
        )

        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ConfirmationCodeSerializer

    def create(self, request):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        code = request.data.get('confirmation_code')
        user_confirmation_code = get_object_or_404(СonfirmationСode, user=user)
        print(code, user_confirmation_code.code)

        if code == user_confirmation_code.code:
            user.is_active = True
            user_confirmation_code.delete()
            refresh = RefreshToken.for_user(user)
            token = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(token, status=status.HTTP_200_OK)

        return Response({'message': 'неверный код подтверждения.'},
                        status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class UserView(mixins.RetrieveModelMixin, mixins.ListModelMixin,
               viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def retrieve(self, request, *args, **kwargs):
        username = kwargs.get('pk')
        if username == 'me':
            if request.user.is_authenticated:
                username = request.user.username
            else:
                return Response({'error': 'пользователь не аутентифицирован'},
                                status=status.HTTP_401_UNAUTHORIZED)
        user = self.queryset.get(username=username)
        if user is None:
            return Response({'error': 'пользователь не найден'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)
