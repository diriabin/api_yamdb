import random

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.handlers import exception
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from api_yamdb.settings import DEFAULT_EMAIL, CONF_CODE_MAX_LEN, DIGS
from .filters import TitleFilter
from .permissions import (IsAdmin, IsAdminModeratorOwnerOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTokenSerializer,
    NotAdminSerializer,
    ReviewSerializer,
    SignUpSerializer,
    TitleReadSerializer, TitleWriteSerializer,
    UserSerializer
)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        Avg('reviews__score')
    ).order_by(
        Title._meta.ordering[0]
    ).select_related(
        'category'
    ).prefetch_related(
        'genre'
    )
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    http_method_names = ('get', 'patch', 'post', 'delete')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class PermittedMethodsAndSearchFilterViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    http_method_names = ('get', 'patch', 'post', 'delete')


class CategoryViewSet(PermittedMethodsAndSearchFilterViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(PermittedMethodsAndSearchFilterViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    http_method_names = ('get', 'patch', 'post', 'delete')
    serializer_class = ReviewSerializer

    def get_tile(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_tile().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_tile())


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)
    http_method_names = ('get', 'patch', 'post', 'delete')
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'patch', 'post', 'delete')

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path=settings.URL_MY_PAGE)
    def get_current_user_info(self, request):
        if request.method == 'GET':
            return Response(
                UserSerializer(request.user).data,
                status=status.HTTP_200_OK
            )
        serializer = NotAdminSerializer(
            request.user,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        user.confirmation_code = (random.choice(DIGS) for _ in range(
            CONF_CODE_MAX_LEN))
        raise exception.BadRequest()


class APISignup(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get('email')
        username = request.data.get('username')
        user_by_name = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_email:
            if username != user_by_email.username:
                return Response(
                    {'Пользователь с таким email почты уже зарегистрирован.'},
                    status=status.HTTP_400_BAD_REQUEST)
        if user_by_name:
            if email != user_by_name.email:
                return Response(
                    {'Пользователь с таким именем уже зарегистрирован.'},
                    status=status.HTTP_400_BAD_REQUEST)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = (random.choice(DIGS) for _ in range(
            CONF_CODE_MAX_LEN))
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            subject='Код подтверждения YaMDb',
            message=f'Ваш код подтверждения: {confirmation_code}',
            from_email=DEFAULT_EMAIL,
            recipient_list=(email,),
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
