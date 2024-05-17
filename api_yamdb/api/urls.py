from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet,
                    CreateUserView, GetTokenView, UserView)

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'genres/?(?P<slug>)', GenreViewSet, basename='genres')
router_v1.register(r'categories/?(?P<slug>)', CategoryViewSet, basename='categories')
router_v1.register(r'auth/signup', CreateUserView, basename='create_user')
router_v1.register(r'auth/token', GetTokenView, basename='get_token')
router_v1.register(r'users', UserView, basename='get_token')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
