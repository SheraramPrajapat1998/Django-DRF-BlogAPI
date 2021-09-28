from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    Checks if current user is `author` of the object or not
    and gives read or write permission based on it.
    """
    message = 'You are not author of this object'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.author


class IsUserOrSuperUserOrReadOnly(BasePermission):
    """
    Checks if current user is `user` of the object or `superuser` or not
    and gives read or write permission based on it.
    """
    message = "You are not the user of this object."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj or request.user.is_superuser
