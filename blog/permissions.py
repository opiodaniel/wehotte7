from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # SAFE METHODS means: GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only the owner can update/delete
        return obj.owner == request.user
