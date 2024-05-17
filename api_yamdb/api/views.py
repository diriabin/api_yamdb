from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from reviews.models import Category, Genre, Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthorOrReadOnly,)
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
