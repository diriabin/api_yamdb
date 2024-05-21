from rest_framework import permissions


# class IsAdminOrReadOnly(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         return (request.method in permissions.SAFE_METHODS or (
#                 request.user.is_authenticated and (
#                     request.user.role == 'admin')))
#
#
# class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#         )
#
#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or obj.author == request.user
#             or request.user.role in ('admin', 'moderator')
#         )
#
#
# class IsAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and (
#             request.user.role == 'admin' or request.user.is_superuser)
#
#     def has_object_permission(self, request, view, obj):
#         return request.user.is_authenticated and (
#             request.user.role == 'admin'
#             or request.user.is_superuser
#         )


class IsAdmin(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminModeratorOwnerOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )