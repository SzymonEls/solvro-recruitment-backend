from rest_framework import permissions

from .models import Cocktail


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        cocktail = obj if isinstance(obj, Cocktail) else obj.cocktail
        return cocktail.author == request.user