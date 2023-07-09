from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwner(BasePermission):
    message = "Доступ для изменения только для создателя или модератора"

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Instance must have an attribute named `owner`.
        if hasattr(obj, "owner"):
            return obj.owner == request.user
        else:
            return False
