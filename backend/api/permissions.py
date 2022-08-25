
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
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_staff