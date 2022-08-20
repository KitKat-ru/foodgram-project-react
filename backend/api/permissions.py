
from rest_framework import permissions


class ObjectReadOnly(permissions.BasePermission):
    """Базовый пермишен, разрешает только безопасные запросы к объектам.
    """
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class AuthorOrReadOnly(ObjectReadOnly):
    """
    Изменять и удалять объект может его автор, модератор или админ.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_authenticated:
            return user == obj.author or user.is_admin or user.is_moderator
        return super().has_object_permission(request, view, obj)