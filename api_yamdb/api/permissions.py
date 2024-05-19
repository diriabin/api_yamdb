from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or (
                request.user.is_authenticated and (
                    request.user.role == 'admin')))


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return True


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser)
