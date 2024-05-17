import random

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          UserSerializer, ConfirmationCodeSerializer)
from reviews.models import Category, Genre, Title
from users.models import СonfirmationСode

User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = TitleSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_destroy(self, serializer):
        obj = get_object_or_404(Genre, slug=self.kwargs.get('slug'))
        obj.delete()
        super(GenreViewSet, self).perform_destroy(serializer)


class CategoryViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_destroy(self, serializer):
        obj = get_object_or_404(Genre, slug=self.kwargs.get('slug'))
        obj.delete()
        super(CategoryViewSet, self).perform_destroy(serializer)


class CreateUserView(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        code = random.randint(100, 999)
        СonfirmationСode.objects.create(user=user, code=code)

        send_mail(
            subject='Код для регистрации',
            message=f'confirmation_code: {code}, username: {username}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.data.get('email')],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(CreateModelMixin, GenericViewSet):
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

        return Response({"message": "неверный код подтверждения."},
                        status=status.HTTP_400_BAD_REQUEST)
