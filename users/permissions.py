from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import User


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return (request.user.role == User.UserRole.ADMIN
                    or request.user.is_superuser)
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return (request.user.role == User.UserRole.ADMIN
                or request.user.is_superuser)


class IsAdminOrModer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        return (
            obj.author == request.user
            or request.user.role == User.UserRole.ADMIN
            or request.user.role == User.UserRole.MODERATOR)
