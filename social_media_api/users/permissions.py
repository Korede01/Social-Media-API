from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission to allow only owners of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.method in ('GET', 'HEAD', 'OPTIONS')
