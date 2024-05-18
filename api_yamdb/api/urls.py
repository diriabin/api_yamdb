from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, UserViewSet,
                    genre_delete, category_delete, CreateUserView,
                    GetTokenView, ReviewViewSet, CommentViewSet)

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'auth/signup', CreateUserView, basename='create_user')
router_v1.register(r'auth/token', GetTokenView, basename='get_token')
router_v1.register(r'users', UserViewSet, basename='get_token')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/genres/<slug:genre_slug>/', genre_delete),
    path('v1/categories/<slug:category_slug>/', category_delete),
]
