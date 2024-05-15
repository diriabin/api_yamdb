from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsAuthorOrReadOnly
from .serializers import TitleSerializer
from reviews.models import Title


class TitleViewSet(viewsets.ViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = TitleSerializer
    permission_classes = IsAuthorOrReadOnly

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
